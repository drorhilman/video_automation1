# Video Frame Fixer

## Description

This Python script allows you to manipulate video frames using OpenCV. It provides various functionalities to adjust video properties like zoom, sharpening, contrast, and more. Additionally, it comes with a Tkinter-based GUI for easier interaction.

## Dependencies

- OpenCV (`cv2`)
- NumPy (`numpy`)
- tqdm (`tqdm`)
- Tkinter (`tkinter`)

## Features

- **Zoom**: Adjust the zoom level of the video frames.
- **Sharpen**: Sharpen the video frames.
- **Contrast**: Adjust the contrast level.
- **Saturation**: Modify the saturation level.
- **Shadow**: Add shadows to the video frames.
- **Highlight**: Add highlights to the video frames.

### Additional Features

- Adjust the speed of the video.
- Resize the frames.
- UI sliders for real-time adjustments.

## Usage

To use this script, clone the repository and run `main()` from the script.

1. Clone the repository
2. Navigate to the directory where the script is located.
3. Run the script:
   ```bash
   python script_name.py
   ```

### Input Parameters

- Source Path: Directory containing the video files to be processed.
- Target Path: Directory where the processed video files will be saved.
- Speed, Zoom, Sharpen, Contrast, Saturation, Shadow, Highlight: Adjust these parameters using sliders in the GUI.
- Width and Height: Set the dimensions for the output video frames.

## Output

The processed videos will be saved in the directory specified in the "Target Path" field.

