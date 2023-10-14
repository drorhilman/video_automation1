
# Using H.264 Encoder to Compress MP4 Video on Windows

## Prerequisites
- FFmpeg installed and accessible via Command Prompt

## Basic Compression Command

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Explanation

- `-i input.mp4`: Specifies the input video file.
- `-c:v libx264`: Sets the codec for the video to H.264.
- `-crf 23`: Sets the Constant Rate Factor (CRF) which controls the quality.

## Optional Parameters

### Preset Option

To change the encoding speed-to-compression ratio:

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset veryfast -crf 23 output.mp4
```

### Bitrate Option

To specify a bitrate:

```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 1M output.mp4
```
