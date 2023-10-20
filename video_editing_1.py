from pathlib import Path
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
import builtins
from tqdm import tqdm
from image_editing_functions import speed, fix_frame
import tkinter as tk
from tkinter import ttk
from ui_functions import center_window, create_slider, create_entry_with_label

# custom CONST:
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# DEFAULT_SOURCE = "C:\\Users\\Ben\\Desktop\\before"
# DEFAULT_TARGET = "C:\\Users\\Ben\\Desktop\\after"

DEFAULT_SOURCE = "/home/dror/personal/ben_video_automation/test/input"
DEFAULT_TARGET = "/home/dror/personal/ben_video_automation/test/output"

# ==========================   UI     ================================


def run_script():
    file_paths = list(Path(builtins.source_path_entry.get()).glob("*.*"))
    target_path = builtins.target_path_entry.get()
    speed_percentage = float(builtins.speed_slider[0].get())
    width = int(builtins.width_entry.get())
    height = int(builtins.height_entry.get())
    params = {
        "width": width,
        "height": height,
        "zoom_percentage": float(builtins.zoom_slider[0].get()),
        "sharpen_percentage": float(builtins.sharpen_slider[0].get()),
        "contrast_percentage": float(builtins.contrast_slider[0].get()),
        "saturation_percentage": float(builtins.saturation_slider[0].get()),
        "shadow_percentage": float(builtins.shadow_slider[0].get()),
        "highlight_percentage": float(builtins.highlight_slider[0].get()),
    }

    for file_path in tqdm(file_paths):
        print(f"{file_path}: {os.path.getsize(file_path) / 1024000:.3f} MB")

        video_capture = cv2.VideoCapture(str(file_path))
        new_frame_rate = speed(video_capture, percentage=speed_percentage)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        output_path = (
            str(Path(target_path) / file_path.name)
            .replace(".mov", ".mp4")
            .replace(".MOV", ".mp4")
        )
        out = cv2.VideoWriter(output_path, fourcc, new_frame_rate, (width, height))

        for _ in tqdm(list(range(total_frames))[:10]):
            ret, frame = video_capture.read()
            if not ret:
                break

            frame = fix_frame(frame, **params)
            out.write(frame)

        # Release resources
        video_capture.release()
        out.release()

        # --------------------------------
        print(f"{file_path}: {os.path.getsize(file_path) / 1024000:.3f} MB")

    cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    root.title("Video Frame Fixer")
    center_window(root, 500, 600)

    builtins.source_path_entry = create_entry_with_label(
        root, "Source Path", DEFAULT_SOURCE
    )
    builtins.target_path_entry = create_entry_with_label(
        root, "Target Path", DEFAULT_TARGET
    )

    builtins.speed_slider = create_slider(root, "Speed %", -100, 100, -20)
    builtins.zoom_slider = create_slider(root, "Zoom %", 0, 100, 60)
    builtins.sharpen_slider = create_slider(root, "Sharpen %", -100, 100, 0.1)
    builtins.contrast_slider = create_slider(root, "Contrast %", -100, 100, 3)
    builtins.saturation_slider = create_slider(root, "Saturation %", -100, 100, -20)
    builtins.shadow_slider = create_slider(root, "Shadow %", -100, 100, 0)
    builtins.highlight_slider = create_slider(root, "Highlight %", -100, 100, 0)

    builtins.width_entry = create_entry_with_label(root, "width:", "1920")
    builtins.height_entry = create_entry_with_label(root, "height:", "1080")

    ttk.Button(root, text="Start", command=run_script).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
