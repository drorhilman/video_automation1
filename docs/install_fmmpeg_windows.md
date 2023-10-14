
# Installing FFmpeg CLI on Windows

## Prerequisites
- Windows 10 or later

## Steps

### 1. Download FFmpeg Executable
Download the FFmpeg executable suitable for your system architecture (32-bit or 64-bit) from the official website: [FFmpeg Downloads](https://ffmpeg.org/download.html).

### 2. Extract Files
After downloading, extract the .zip files. You should find a folder named `ffmpeg-X.X.X-winXX-static` (or similar).

### 3. Move FFmpeg Folder
Move this folder to a location you prefer, e.g., `C:\Program Files\`.

### 4. Add to Environment Variables
1. Go to `Control Panel` > `System` > `Advanced system settings` > `Environment Variables`.
2. Under `System Variables`, find `Path` and click `Edit`.
3. Add the path to the `bin` directory inside the `ffmpeg-X.X.X-winXX-static` folder. E.g., `C:\Program Files\ffmpeg-X.X.X-winXX-static\bin`.

### 5. Verify Installation
Open Command Prompt and run:

```bash
ffmpeg -version
```

If you see version information, FFmpeg has been installed successfully.
