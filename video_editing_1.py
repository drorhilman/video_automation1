from pathlib import Path
import ctypes
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
import builtins
from tqdm import tqdm


fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# fourcc = cv2.VideoWriter_fourcc(*'H264')


def zoom(frame, percentage=60):
    h, w, _ = frame.shape
    crop_margin_x = w * ((100 - percentage) / 100) / 2
    crop_margin_y = h * ((100 - percentage) / 100) / 2
    x1 = int(crop_margin_x)
    y1 = int(crop_margin_y)
    x2 = int(w - crop_margin_x)
    y2 = int(h - crop_margin_y)
    return frame[y1:y2, x1:x2]


def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))


def sharpen_image(frame, percentage):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    scaled_kernel = kernel * ((100 -percentage) / 100)
    return cv2.filter2D(frame, -1, scaled_kernel)

def speed(video_capture, percentage=30):
    original_frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    new_frame_rate = original_frame_rate * (100 + percentage) / 100
    return new_frame_rate

def adjust_contrast(frame, percentage):
    alpha= (100 + percentage) / 100
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=0)


def adjust_saturation(frame, percentage):
    saturation_scale = (100 + percentage)/100
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.convertScaleAbs(s, alpha=saturation_scale, beta=0)
    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def add_shadow(frame, percentage):
    shadow_intensity = percentage / 100.0
    shadow_frame = frame * (1 - shadow_intensity)
    return shadow_frame.astype(np.uint8)

def add_highlight(frame, percentage):
    highlight_intensity = percentage / 100.0
    highlight_frame = frame + (255 - frame) * highlight_intensity
    np.clip(highlight_frame, 0, 255, out=highlight_frame)
    return highlight_frame.astype(np.uint8)


def print_size(file_path):
    original_size = os.path.getsize(file_path) / 1024000
    print(f"{file_path}: {original_size:.3f} MB")

def fix_frame(frame, zoom_percentage=60, sharpen_percentage=0.1, contrast_percentage=3, 
               saturation_percentage=-20, width=1920, height=1080, shadow_percentage=0, highlight_percentage=0):
    frame = zoom(frame, percentage=zoom_percentage)
    frame = sharpen_image(frame, percentage=sharpen_percentage)
    frame = adjust_contrast(frame, percentage=contrast_percentage)
    frame = adjust_saturation(frame, percentage=saturation_percentage)
    if shadow_percentage != 0:
        frame = add_shadow(frame, shadow_percentage)
    if highlight_percentage != 0:
        frame = add_highlight(frame, highlight_percentage )
    frame = resize_frame(frame, width=width, height=height)
    return frame


import tkinter as tk
from tkinter import ttk

def create_slider(root, label, from_, to_, initial_value):
    frame = tk.Frame(root, padx=10, pady=2)  # Create a frame with padding
    frame.pack(padx=20, pady=2)
    
    ttk.Label(frame, text=label).pack(side=tk.LEFT)
    
    var = tk.StringVar()
    var.set(initial_value)
    
    def update_slider(val):
        slider.set(float(var.get()))
        
    def update_var(val):
        var.set(str(slider.get()))
        
    entry = ttk.Entry(frame, textvariable=var, width=10)
    entry.pack(side=tk.RIGHT)
    
    slider = ttk.Scale(frame, from_=from_, to_=to_, orient='horizontal')
    slider.set(initial_value)
    slider.pack(fill=tk.X, side=tk.RIGHT)
    
    var.trace_add("write", lambda *args: update_slider(var.get()))
    slider.bind("<Motion>", lambda *args: update_var(slider.get()))
    
    return slider, var


def create_entry_with_label(root, label_text, initial_value, width=200, padx=10, pady=2):
    ttk.Label(root, text=label_text).pack(padx=padx, pady=pady)
    entry = ttk.Entry(root, width=width)
    entry.insert(0, initial_value)
    entry.pack(fill=tk.X, padx=padx, pady=pady)
    return entry


def center_window(root, width=500, height=400):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f'{width}x{height}+{x}+{y}')


def run_script():
    file_paths = list(Path(builtins.source_path_entry.get()).glob("*.*"))
    target_path = builtins.target_path_entry.get()
    speed_percentage = float(builtins.speed_slider[0].get())
    width = int(builtins.width_entry.get())
    height = int(builtins.height_entry.get())
    params = {
        "width" : width,
        "height" : height,
        "zoom_percentage" : float(builtins.zoom_slider[0].get()),
        "sharpen_percentage" : float(builtins.sharpen_slider[0].get()),
        "contrast_percentage" : float(builtins.contrast_slider[0].get()),
        "saturation_percentage" : float(builtins.saturation_slider[0].get()),
        "shadow_percentage" : float(builtins.shadow_slider[0].get()),
        "highlight_percentage" : float(builtins.highlight_slider[0].get()),
    }


    for file_path in tqdm(file_paths):
        print_size(file_path)

        video_capture = cv2.VideoCapture(str(file_path))
        new_frame_rate = speed(video_capture, percentage=speed_percentage)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        output_path = str(Path(target_path) / file_path.name).replace(".mov",".mp4").replace(".MOV",".mp4")
        out = cv2.VideoWriter(str(output_path), fourcc, new_frame_rate , (width, height))

        for _ in tqdm(range(total_frames)):
            ret, frame = video_capture.read()
            if not ret:
                break
            
            frame = fix_frame(frame, **params)
            out.write(frame)

        # Release resources
        video_capture.release()
        out.release()
        
        #--------------------------------
        print_size(output_path)

    cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    root.title('Video Frame Fixer')
    center_window(root, 500, 600)

    builtins.source_path_entry = create_entry_with_label(root, "Source Path", "C:\\Users\\Ben\\Desktop\\before")
    builtins.target_path_entry = create_entry_with_label(root, "Target Path", "C:\\Users\\Ben\\Desktop\\after")
    builtins.speed_slider = create_slider(root, 'Speed %', -100, 100, -20)

    builtins.zoom_slider = create_slider(root, 'Zoom %', 0, 100, 60)
    builtins.sharpen_slider = create_slider(root, 'Sharpen %', -100, 100, 0.1)
    builtins.contrast_slider = create_slider(root, 'Contrast %', -100, 100, 3)
    builtins.saturation_slider = create_slider(root, 'Saturation %', -100, 100, -20)
    builtins.shadow_slider = create_slider(root, 'Shadow %', -100, 100, 0)
    builtins.highlight_slider = create_slider(root, 'Highlight %', -100, 100, 0)

    builtins.width_entry = create_entry_with_label(root, "רוחב:", "1920")
    builtins.height_entry = create_entry_with_label(root, "אורך:", "1080")

    ttk.Button(root, text='Start', command=run_script).pack()

    root.mainloop()


if __name__ == "__main__":
    main()


