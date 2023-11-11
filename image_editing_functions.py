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
    # Convert the image from RGB to LAB color space
    percentage_fix = 300.0
    lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    # Create a softer mask for highlights
    # The mask intensity is proportional to the brightness above a certain threshold
    highlight_threshold = 100  # Lower threshold for a more gradual effect
    soft_mask = np.clip((l_channel - highlight_threshold) / (255 - highlight_threshold), 0, 1)

    # Calculate the adjustment factor based on the percentage
    adjustment_factor = 1 + (percentage / percentage_fix)

    # Apply the adjustment factor using the soft mask
    l_channel_adjusted = l_channel * (1 + soft_mask * (adjustment_factor - 1))

    # Ensure l_channel_adjusted is the same data type and size as the original l_channel
    l_channel_adjusted = np.clip(l_channel_adjusted, 0, 255).astype(np.uint8)

    # Merge the adjusted L channel back with the A and B channels
    adjusted_lab = cv2.merge([l_channel_adjusted, a_channel, b_channel])
    adjusted_frame = cv2.cvtColor(adjusted_lab, cv2.COLOR_LAB2RGB)

    return adjusted_frame



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
