from pathlib import Path
import cv2
import os
import builtins
from tqdm import tqdm
from image_editing_functions import speed, fix_frame, compress_with_ffmpg
import customtkinter as ctk  # type: ignore


from ui_functions import (
    center_window,
    create_slider,
    create_entry_with_label,
    display_frame,
    get_params_from_ui,
    update_loaded_frame,
    load_first_frame,
    update_frame_loading_on_params_change,
)

# custom CONST:
fourcc = cv2.VideoWriter_fourcc(*"mp4v") # type: ignore
DEFAULT_SOURCE = "C:\\Users\\Ben\\Desktop\\before"
DEFAULT_TARGET = "C:\\Users\\Ben\\Desktop\\after"
MAX_FRAMES = 100000000

if Path("test/input").exists():
    DEFAULT_SOURCE = "test/input"
    DEFAULT_TARGET = "test/output"
    MAX_FRAMES = 100
# ==========================   UI     ================================


def run_script():
    file_paths = list(Path(builtins.source_path_entry.get()).glob("*.*"))
    target_path = builtins.target_path_entry.get()
    speed_percentage = float(builtins.speed_slider[0].get())
    params, width, height = get_params_from_ui()
    builtins.message.configure(text="Running...")

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

        for _ in tqdm(list(range(total_frames)[:MAX_FRAMES])):
            ret, frame = video_capture.read()
            if not ret:
                break

            frame = fix_frame(frame, **params)
            out.write(frame)
            # if i == 240: break

        # Release resources
        video_capture.release()
        out.release()

        # --------------------------------
        print(f"{file_path}: {os.path.getsize(file_path) / 1024000:.3f} MB")
        print(f"Compressing {output_path}... into {output_path}_compressed.mp4")
        compress_with_ffmpg(output_path, f"{output_path}_compressed.mp4")

    cv2.destroyAllWindows()

    # Now compress the file with ffmpeg


def main():
    root = ctk.CTk()
    root.title("Video Frame Fixer")

    left_width, right_width = 300, 800

    left_frame = ctk.CTkFrame(root, width=left_width)
    left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)
    builtins.update_loaded_frame = update_loaded_frame
    # Add widgets to the left frame
    builtins.source_path_entry = create_entry_with_label(
        left_frame, "Source Path", DEFAULT_SOURCE
    )
    builtins.target_path_entry = create_entry_with_label(
        left_frame, "Target Path", DEFAULT_TARGET
    )

    buttons_frame = ctk.CTkFrame(left_frame)
    buttons_frame.pack(pady=5, fill=ctk.X)
    ctk.CTkButton(
        buttons_frame, text="Original Frame", command=load_first_frame, fg_color="grey"
    ).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(
        buttons_frame,
        text="Apply Fix",
        command=update_loaded_frame,
        fg_color="grey",
    ).pack(side=ctk.LEFT, padx=10)

    builtins.speed_slider = create_slider(left_frame, "Speed %", -100, 100, 20)
    builtins.zoom_slider = create_slider(left_frame, "Zoom %", 0, 100, 60)
    builtins.shift_left = create_slider(left_frame, "Shift →", -500, 500, 0)
    builtins.shift_down = create_slider(left_frame, "shift ↓ ", -500, 500, 0)
    builtins.sharpen_slider = create_slider(left_frame, "Sharpen %", -100, 100, 0)
    builtins.contrast_slider = create_slider(left_frame, "Contrast %", -100, 100, 3)
    builtins.saturation_slider = create_slider(
        left_frame, "Saturation %", -100, 100, -20
    )
    builtins.shadow_slider = create_slider(left_frame, "Shadow %", -100, 100, 0)
    builtins.highlight_slider = create_slider(left_frame, "Highlight %", -100, 100, 0)

    builtins.width_entry = create_entry_with_label(left_frame, "width:", "3840")
    builtins.height_entry = create_entry_with_label(left_frame, "height:", "2160")

    # start button
    ctk.CTkButton(left_frame, text="Start", command=run_script).pack()

    # comments label:
    messages_frame = ctk.CTkFrame(left_frame)
    messages_frame.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True)
    builtins.message = ctk.CTkLabel(messages_frame, text="Not started", width=100)
    builtins.message.pack()

    # -----------------------------------------------------------
    builtins.right_frame = ctk.CTkFrame(root, width=right_width)
    builtins.right_frame.pack(
        side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True
    )

    center_window(root, width=left_width + right_width, height=600)

    def repeat_update(time=200):
        update_frame_loading_on_params_change()
        root.after(time, repeat_update)

    repeat_update()

    root.mainloop()


if __name__ == "__main__":
    main()
