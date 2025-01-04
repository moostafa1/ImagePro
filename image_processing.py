import cv2
import numpy as np

# Helper functions
def adjust_image(image, contrast: float, brightness: int):
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def edge_detection(image, min_thresh, max_thresh):
    return cv2.Canny(image, min_thresh, max_thresh)

def denoise_image(image, method: str, **kwargs):
    if method == "gaussian":
        kernel_size_w = kwargs.get("kernel_size_w", 5)
        kernel_size_h = kwargs.get("kernel_size_h", 5)
        return cv2.GaussianBlur(image, (kernel_size_w, kernel_size_h), 0)

    elif method == "median":
        kernel_size = kwargs.get("kernel_size", 5)
        return cv2.medianBlur(image, kernel_size)

    elif method == "bilateral":
        diameter = kwargs.get("diameter", 9)
        sigma_color = kwargs.get("sigma_color", 75)
        sigma_space = kwargs.get("sigma_space", 75)
        return cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)

    elif method == "nlm":  # Non-Local Means Denoising
        h = kwargs.get("h", 10)
        template_window_size = kwargs.get("template_window_size", 7)
        search_window_size = kwargs.get("search_window_size", 21)
        return cv2.fastNlMeansDenoisingColored(image, None, h, h, template_window_size, search_window_size)

    else:
        raise ValueError(f"Unsupported denoising method: {method}")


def convert_color(image, color_space: str):
    if color_space == "GRAY":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif color_space == "HSV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_space == "RGB":
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif color_space == "BGR":
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGR)
    elif color_space == "YUV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    elif color_space == "YCrCb":
        return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    elif color_space == "HLS":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    elif color_space == "LAB":
        return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    elif color_space == "LUV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
    elif color_space == "XYZ":
        return cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
    else:
        raise ValueError("Unsupported color space")


def threshold_image(image, min_threshold: int, max_threshold: int):
    return cv2.threshold(image, min_threshold, max_threshold, cv2.THRESH_BINARY)[1]

def rotate_image(image, angle: float):
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, rotation_matrix, (w, h))

def resize_image(image, width: int, height: int):
    return cv2.resize(image, (width, height))

def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray)

def face_detection(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return image

def apply_filter(image, filter_type: str):
    if filter_type == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.filter2D(image, -1, kernel)
        return np.clip(sepia, 0, 255)
    else:
        raise ValueError("Unsupported filter type")

def add_text(image, text: str, x: int, y: int):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return image

def select_roi(image, x: int, y: int, w: int, h: int):
    return image[y:y+h, x:x+w]

def flip_image(image, axis: str):
    if axis == "horizontal":
        axis = 0
    elif axis == "vertical":
        axis = 1
    return cv2.flip(image, axis)

def high_pass_filter(image, blur_radius: int):
    blurred = cv2.GaussianBlur(image, (blur_radius, blur_radius), 0)
    high_pass = cv2.subtract(image, blurred)
    return cv2.convertScaleAbs(high_pass)


def sobel_sharpen(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    combined = cv2.magnitude(sobelx, sobely)
    return cv2.convertScaleAbs(combined)

def detect_card(image, card_contour_points):
    # Get the perspective transform
    pts = np.array(card_contour_points, dtype="float32")

    # Define the order of points (top-left, top-right, bottom-right, bottom-left)
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left
    rect[2] = pts[np.argmax(s)]  # Bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-right
    rect[3] = pts[np.argmax(diff)]  # Bottom-left

    # Define the width and height of the card
    width = max(np.linalg.norm(rect[0] - rect[1]), np.linalg.norm(rect[2] - rect[3]))
    height = max(np.linalg.norm(rect[0] - rect[3]), np.linalg.norm(rect[1] - rect[2]))

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (int(width), int(height)))
    return warped
