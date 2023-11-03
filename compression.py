import subprocess
from tqdm import tqdm
import re
import builtins

progress_pattern = re.compile(r"time=(\d+:\d+:\d+\.\d+)")


# First, get the total duration using ffprobe
def duration_command(input_file: str):
    return [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_file,
    ]


def compress_with_ffmpeg(input_file: str, output_file: str, target_bitrate="4000k", crf_value="32"):
    duration_output = subprocess.run(duration_command(input_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    total_duration = float(duration_output.stdout)

    # Now start the ffmpeg process
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Overwrite without asking if the output file exists
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-b:v",
        target_bitrate,
        "-crf",
        crf_value,
        "-preset",
        "slow",  # A slower preset will provide better compression
        "-an",
        output_file,
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Initialize tqdm progress bar
    with tqdm(total=total_duration, unit="s") as bar:
        while True:
            line = process.stderr.readline()
            if not line:
                break
            if match := progress_pattern.search(line):
                time_str = match.group(1)
                hours, minutes, seconds = map(float, time_str.split(":"))
                current_time = hours * 3600 + minutes * 60 + seconds
                setattr(builtins, "compression", current_time)
                bar.update(current_time - bar.n)  # update progress bar

    # Check if the compression finished successfully
    setattr(builtins, "compression", "started")
    process.wait()  # Wait for the ffmpeg process to finish
    if process.returncode == 0:
        setattr(builtins, "compression", "Done")
        print("Compression finished successfully.")
    else:
        setattr(builtins, "compression", "error")
        print("Compression failed with return code", process.returncode)
        print("Error message:", process.stderr.read())
