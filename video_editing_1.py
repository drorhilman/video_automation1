from pathlib import Path
import cv2
import os
import builtins
from tqdm import tqdm
from image_editing_functions import fix_frame
from compression import compress_with_ffmpeg
import customtkinter as ctk  # type: ignore
import threading
from tqdm.contrib.concurrent import process_map  # type: ignore
import shutil


from ui_functions import (
    center_window,
    create_slider,
    create_entry_with_label,
    get_params_from_ui,
    update_loaded_frame,
    load_first_frame,
    update_frame_loading_on_params_change,
)

# custom CONST:
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
DEFAULT_SOURCE = "C:\\Users\\Ben\\Desktop\\before"
DEFAULT_TARGET = "C:\\Users\\Ben\\Desktop\\after"
MAX_FRAMES = 100000000
BITRATE = "4000k"


def skip_frame(frame_idx: int, speed_percentage: float) -> bool:
    if speed_percentage == 0:
        return False  # No skipping if speed is 100%

    # e.g., 30% increase means 1.3 times the original frame rate
    frame_rate_multiplier = 1 + (speed_percentage / 100)

    # Calculate the skip factor, For 130% speed, we want to keep 100/130 of the frames
    skip_factor = 1 - (1 / frame_rate_multiplier)

    # Now, we skip frames based on the skip factor. We skip a frame if the current index divided by total frames is less than skip factor
    return (frame_idx % int(1 / skip_factor)) != 0


if Path("test/input").exists():
    DEFAULT_SOURCE = "test/input"
    DEFAULT_TARGET = "test/output"
    MAX_FRAMES = 100
# ==========================   UI     ================================
# Global flag to check if the script should stop
stop_script = False


def process_video_frame(video_capture, params):
    ret, frame = video_capture.read()
    return fix_frame(frame, **params) if ret else None


def fix_frame_process(params):
    frame, params = params
    return fix_frame(frame, **params)


def run_script():
    global stop_script
    file_paths = list(Path(builtins.source_path_entry.get()).glob("*.*"))
    target_path = builtins.target_path_entry.get()
    speed_percentage = float(builtins.speed_slider[0].get())
    params, width, height = get_params_from_ui()
    MAX_FRAMES = params["max_frames"]
    builtins.message.configure(text="Running...")

    for file_path in tqdm(file_paths, desc="Files"):
        if stop_script:
            break
        print(f"{file_path}: {os.path.getsize(file_path) / 1024000:.3f} MB")

        output_path = process_video(
            target_path, speed_percentage, params, width, height, MAX_FRAMES, file_path
        )
        if stop_script:
            return
        # --------------------------------
        print(f"{file_path}: {os.path.getsize(file_path) / 1024000:.3f} MB")
        print(f"Compressing {output_path}... into {output_path}_compressed.mp4")
        builtins.message.configure(text=f"Compressing Image: {Path(file_path).name} ")
        compress_with_ffmpeg(
            output_path,
            f"{output_path}_compressed.mp4",
            target_bitrate=builtins.bitrate.get(),
        )

        # rename the compressed file to the original name, deletign the original...
        shutil.move(f"{output_path}_compressed.mp4", output_path)

    stop_script = False
    builtins.message.configure(text="Done!")

    cv2.destroyAllWindows()


def process_video(
    target_path, speed_percentage, params, width, height, MAX_FRAMES, file_path
):
    video_capture = cv2.VideoCapture(str(file_path))

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frame_rate = int((speed_percentage+100)/100 * frame_rate)
    output_path = fix_output_path_name(target_path, file_path)
    out = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))
    
    frame_count = list(range(min(total_frames, MAX_FRAMES)))
    for _ in tqdm(frame_count, desc="Loading Frames"):
        if not stop_script:
            frame = video_capture.read()[1]
            fixed = fix_frame_process((frame, params))
            out.write(fixed)
    

        # Release resources
    video_capture.release()
    out.release()
    return output_path


def fix_output_path_name(target_path, file_path):
    return (
        str(Path(target_path) / file_path.name)
        .replace(".mov", ".mp4")
        .replace(".MOV", ".mp4")
    )

    # Now compress the file with ffmpeg


def stop_running():
    global stop_script
    stop_script = True
    builtins.stop_button.pack_forget()
    builtins.start_button.pack(side=ctk.LEFT, padx=10)
    builtins.message.configure(text="Stopped!")


def start_script():
    global stop_script
    stop_script = False

    builtins.message.configure(text="Running...")
    builtins.start_button.pack_forget()
    builtins.stop_button.pack(side=ctk.LEFT, padx=10)
    threading.Thread(target=run_script).start()


def main():
    root = ctk.CTk()
    root.title("Video Frame Fixer")

    left_width, right_width = 100, 1400

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

    builtins.speed_slider = create_slider(left_frame, "Speed %", 0, 100, 30)
    builtins.zoom_slider = create_slider(left_frame, "Zoom %", 0, 100, 40)
    builtins.shift_left = create_slider(left_frame, "Shift →", -1000, 1000, 0)
    builtins.shift_down = create_slider(left_frame, "shift ↓ ", -1000, 1000, 0)
    builtins.sharpen_slider = create_slider(left_frame, "Sharpen %", -100, 100, 0)
    builtins.contrast_slider = create_slider(left_frame, "Contrast %", -100, 100, 0)
    builtins.saturation_slider = create_slider(left_frame, "Saturation %", -100, 100, 0)
    builtins.shadow_slider = create_slider(left_frame, "Shadow %", -100, 100, 0)
    builtins.highlight_slider = create_slider(left_frame, "White %", -100, 100, 0)

    builtins.max_frames = create_entry_with_label(left_frame, "max frames:", MAX_FRAMES)
    builtins.bitrate = create_entry_with_label(left_frame, "bitrate:", BITRATE)
    builtins.width_entry = create_entry_with_label(left_frame, "width:", "3840")
    builtins.height_entry = create_entry_with_label(left_frame, "height:", "2160")

    # start button
    start_buttons_frame = ctk.CTkFrame(left_frame)
    start_buttons_frame.pack(pady=5, fill=ctk.X)
    builtins.start_button = ctk.CTkButton(
        start_buttons_frame, text="Start", command=start_script
    )
    builtins.start_button.pack(side=ctk.LEFT, padx=10)
    builtins.stop_button = ctk.CTkButton(
        start_buttons_frame, text="Stop", command=stop_running, fg_color="red"
    )

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

    center_window(root, width=left_width + right_width, height=800)

    def repeat_update(time=100):
        update_frame_loading_on_params_change()
        root.after(time, repeat_update)

    def on_closing():
        global stop_script
        stop_script = True
        root.destroy()
        exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(100, load_first_frame)
    root.after(200, repeat_update)
    root.mainloop()


if __name__ == "__main__":
    main()
