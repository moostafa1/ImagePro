from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import cv2
import numpy as np
from PIL import Image
import base64
import io
from image_processing import adjust_image, adjust_opacity_and_blur, pixelate, hdr_effect, mirror_h, mirror_v, vignette

app = FastAPI()

# Setting up templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Route for the main page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to process the image
@app.post("/adjust")
async def adjust(
    image: UploadFile = File(...), 
    contrast: float = Form(None), 
    brightness: int = Form(None),
    opacity: float = Form(None),
    blur_ksize: int = Form(None),
    flip_h: int = Form(None),
    flip_v: int = Form(None)
):
    try:
        # Read and process the image
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        image_np = np.array(pil_image)

        # Convert the image from RGB to BGR (if needed)
        if image_np.shape[-1] == 4:  # RGBA
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        elif image_np.shape[-1] == 3:  # RGB
            pass  # Already in RGB format
        else:
            raise ValueError("Unsupported image format. Please upload an RGB or RGBA image.")

        # Adjust the image
        adjusted_image = adjust_image(image_np, contrast, brightness)
        adjusted_image = adjust_opacity_and_blur(adjusted_image, opacity, blur_ksize)
        
        if flip_h:
            adjusted_image = mirror_h(adjusted_image)
        if flip_v:
            adjusted_image = mirror_v(adjusted_image)

        # Convert the adjusted image to RGB (to ensure consistency)
        if adjusted_image.shape[-1] == 3:  # BGR format
            adjusted_image_rgb = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
        else:
            adjusted_image_rgb = adjusted_image  # Already in RGB

        # Convert the image to Base64 for display in the browser
        _, buffer = cv2.imencode('.png', adjusted_image_rgb)
        adjusted_image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(content={"image": adjusted_image_base64})
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)