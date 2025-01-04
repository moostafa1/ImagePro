from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import cv2
import numpy as np
from PIL import Image
import base64
import io
from image_processing import adjust_image

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
    contrast: float = Form(...), 
    brightness: int = Form(...)
):
    # Read and process the image
    contents = await image.read()
    pil_image = Image.open(io.BytesIO(contents))
    image_np = np.array(pil_image)
    adjusted_image = adjust_image(image_np, contrast, brightness)

    # Convert the image to Base64 for display in the browser
    _, buffer = cv2.imencode('.png', adjusted_image)
    adjusted_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return JSONResponse(content={"image": adjusted_image_base64})

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
