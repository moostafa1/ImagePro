import cv2
import numpy as np

# Helper functions
def adjust_image(image, contrast: float = None, brightness: int = None):
    """
    Adjust the contrast or brightness of an image.

    :param image: The input image (numpy array)
    :param contrast: Contrast factor (default is None, no change)
    :param brightness: Brightness adjustment value (default is None, no change)
    :return: The adjusted image
    """
    # Set default values if not provided
    alpha = contrast if contrast is not None else 1.0  # Default contrast = 1.0
    beta = brightness if brightness is not None else 0  # Default brightness = 0

    # Apply the adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image


def adjust_opacity_and_blur(image, opacity: float = 1.0, blur_ksize: int = 0):
    """
    Adjust the opacity and blur of an image.

    :param image: The input image (numpy array)
    :param opacity: Opacity factor (0.0 to 1.0). 1.0 is fully opaque, 0.0 is fully transparent.
    :param blur_ksize: Kernel size for blurring. Must be an odd number (e.g., 3, 5, 7).
                       Set to 0 for no blur.
    :return: The adjusted image
    """
    # Ensure opacity is in the range [0.0, 1.0]
    if not (0.0 <= opacity <= 1.0):
        raise ValueError("Opacity must be between 0.0 and 1.0.")
    
    # Adjust opacity
    if opacity < 1.0:
        # Create a transparent overlay
        overlay = np.zeros_like(image)
        image = cv2.addWeighted(image, opacity, overlay, 1 - opacity, 0)

    # Apply blur if kernel size is provided
    if blur_ksize > 0:
        if blur_ksize % 2 == 0:
            raise ValueError("Blur kernel size must be an odd number.")
        image = cv2.GaussianBlur(image, (blur_ksize, blur_ksize), 0)

    return image


def mirror_h(image):
    return cv2.flip(image, 1)  # flip_code=1: horizontal, 0: vertical

def mirror_v(image):
    return cv2.flip(image, 0)  # flip_code=1: horizontal, 0: vertical

def pixelate(image, pixel_size: int):
    (h, w) = image.shape[:2]
    image = cv2.resize(image, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(image, (w, h), interpolation=cv2.INTER_NEAREST)


def hdr_effect(image, ss: int, sr: float):
    return cv2.detailEnhance(image, sigma_s=ss, sigma_r=sr)

def vignette(image, vignette_scale: float):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, vignette_scale * cols)
    kernel_y = cv2.getGaussianKernel(rows, vignette_scale * rows)
    kernel = kernel_y * kernel_x.T
    mask = kernel / kernel.max()
    return (image * mask[:, :, np.newaxis]).astype(np.uint8)