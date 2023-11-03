import cv2
import numpy as np
import builtins


def shift_frame(frame: np.ndarray, x: int, y: int):
    if x == 0 and y == 0:
        return frame
    h, w, _ = frame.shape
    M = np.float32([[1, 0, x], [0, 1, y]])  # type: ignore
    return cv2.warpAffine(frame, M, (w, h), borderValue=[255, 255, 255])  # type: ignore


def sharpen_image(frame: np.ndarray, percentage: float) -> np.ndarray:
    """
    Sharpens the given frame using an unsharp mask with the specified sharpening percentage.
    """
    if percentage == 0:
        return frame
    percentage = max(0, min(100, percentage)) / 100
    frame_float = frame.astype(np.float64)
    blurred = cv2.GaussianBlur(frame_float, (0, 0), sigmaX=3, sigmaY=3)
    sharpened = cv2.addWeighted(frame_float, 1.0 + percentage, blurred, -percentage, 0)
    # Convert the sharpened frame back to uint8 format for displaying or saving
    sharpened = sharpened.astype(np.uint8)
    return sharpened


def zoom(frame: np.ndarray, percentage: int = 60) -> np.ndarray:
    h, w, _ = frame.shape
    percentage = 100-percentage
    crop_margin_x = w * ((100 - percentage) / 100) / 2
    crop_margin_y = h * ((100 - percentage) / 100) / 2
    x1 = int(crop_margin_x)
    y1 = int(crop_margin_y)
    x2 = int(w - crop_margin_x)
    y2 = int(h - crop_margin_y)
    return frame[y1:y2, x1:x2]


def resize_frame(frame: np.ndarray, width: int, height: int):
    return cv2.resize(frame, (width, height))


def sharpen_image_old(frame: np.ndarray, percentage: float):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    scaled_kernel = kernel * ((100 - percentage) / 100)
    return cv2.filter2D(frame, -1, scaled_kernel)


def speed(video_capture, percentage: float = 30):
    original_frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    return original_frame_rate * (100 + percentage) / 100


def adjust_contrast(frame: np.ndarray, percentage: float):
    alpha = (100 + percentage) / 100
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=0)


def adjust_saturation(frame: np.ndarray, percentage: float):
    if percentage == 0:
        return frame
    saturation_scale = (100 + percentage) / 100
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.convertScaleAbs(s, alpha=saturation_scale, beta=0)
    hsv = cv2.merge(np.array([h, s, v]))  # type: ignore
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def add_shadow(frame: np.ndarray, percentage: float):
    if percentage == 0:
        return frame
    shadow_intensity = percentage / 100.0
    shadow_frame = frame * (1 - shadow_intensity)
    return shadow_frame.astype(np.uint8)


def add_highlight(frame: np.ndarray, percentage: float):
    if percentage == 0:
        return frame
    highlight_intensity = percentage / 100.0
    highlight_frame = frame + (255 - frame) * highlight_intensity
    np.clip(highlight_frame, 0, 255, out=highlight_frame)
    return highlight_frame.astype(np.uint8)


def fix_frame(
    frame,
    zoom_percentage=60,
    sharpen_percentage=0.1,
    contrast_percentage=3,
    saturation_percentage=-20,
    width=1920,
    height=1080,
    shadow_percentage=0,
    highlight_percentage=0,
    shift_x=0,
    shift_y=0,
    max_frames=10000000,
):
    frame = shift_frame(frame, shift_x, shift_y)
    frame = zoom(frame, percentage=zoom_percentage)
    frame = sharpen_image(frame, percentage=sharpen_percentage)
    frame = adjust_contrast(frame, percentage=contrast_percentage)
    frame = adjust_saturation(frame, percentage=saturation_percentage)
    if shadow_percentage != 0:
        frame = add_shadow(frame, shadow_percentage)
    if highlight_percentage != 0:
        frame = add_highlight(frame, highlight_percentage)
    if width != 0 and height != 0:
        frame = resize_frame(frame, width=width, height=height)
    return frame


#  ============= DOCS .... ==============================

"""
# The Unsharp Mask (USM) is a popular sharpening technique used in image processing to enhance the apparent sharpness of images. 

Here's a step-by-step explanation of the Unsharp Mask technique:

## Blurring:

    Initially, a blurred version of the original image is created using a Gaussian blur or another blurring filter.
    Subtraction:

    The blurred image is then subtracted from the original image to create a "mask" which represents the detail that was lost during the blurring process.
    Addition:

## Sharpening:

    Finally, this "mask" is added back to the original image, enhancing the high-frequency components (edges, textures), which effectively sharpens the image.
    In formulaic terms, the unsharp mask process can be expressed as follows:

    `Sharpened Image =Original Image + (Original Image−Blurred Image) × Amount`

Here, the "Amount" is a factor that controls the degree of sharpening applied. A higher Amount value results in stronger sharpening, and vice versa.

In the context of digital image processing, the Unsharp Mask technique can accentuate edges and fine details in images, making them appear clearer and more defined. 
This technique is widely used in various software applications and platforms for enhancing image clarity and is a fundamental concept in the domain of image and video processing."""
