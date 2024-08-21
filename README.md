# PWFace Readme

## Overview

This project is a Python-based application that uses audio input to animate a character's mouth in real-time. The character's mouth opens and closes depending on the volume of the sound, simulating speech.. The application is built using the Pygame library for graphics and Pyaudio for audio processing. 

The character's sprite animations can be customized by placing different images in the specified sprite folder. The application also supports basic window management, such as moving the window around the screen by dragging it with the mouse.

## Features

- **Real-time Audio Visualization:** The character's mouth animation reacts to the loudness of the audio input.
- **Customizable Sprites:** Users can customize the appearance of the character by placing different images in the specified sprite folder.
- **Window Management:** The application window can be moved by clicking and dragging with the mouse.
- **Adjustable Audio Sensitivity:** The maximum volume threshold (`maxV`) can be adjusted to better suit different audio input levels.
- **Debug Mode:** Print out various information such as audio loudness and settings to the console for debugging purposes.

## Prerequisites

Before running the application, ensure that you have the following libraries installed:

- `pygame`
- `pyaudio`
- `numpy`
- `pywin32` (for Windows API interaction)

You can install these libraries using `pip`:

```sh
pip install pygame pyaudio numpy pywin32
```

## Configuration

### Variables

- **`Window_Size`**: Sets the size of the application window. Default is `300`.
- **`Reflect`**: Flips the character horizontally if set to `True`.
- **`maxV`**: Maximum volume threshold. If the input audio loudness exceeds this value, it will be clamped to `maxV`.
- **`DebugMode`**: If `True`, the application will print various debug information to the console.
- **`sprite_folder`**: Directory containing the sprite images for the character's mouth animation. Images should be named in a way that allows them to be sorted correctly based on the degree of mouth openness.

### Audio Settings

- **`CHUNK_SIZE`**: Number of audio frames per buffer.
- **`FORMAT`**: Audio format. Default is `pyaudio.paInt16`.
- **`CHANNELS`**: Number of audio channels. Default is `1`.
- **`RATE`**: Sampling rate in Hz. Default is `48000`.

## Setup

1. **Prepare the Sprite Folder:**
   - Place your sprite images in the folder specified by `sprite_folder`. Default is `Sprites`
   - Ensure that the images are named in a way that they sort correctly based on mouth openness.

2. **Adjust Settings:**
   - Modify the `Window_Size`, `Reflect`, `maxV`, and `DebugMode` variables as needed to suit your preferences.

3. **Run the Application:**
   - Execute the Python script to start the application.
   - The application will open a window displaying the character, and the mouth animation will react to the loudness of the audio input.

## Usage

- **Move the Window:**
  - Click and hold the left mouse button within the application window, then drag the mouse to move the window around the screen.

- **Debug Information:**
  - If `DebugMode` is enabled, the console will display the current loudness of the audio input and other relevant settings.

## Troubleshooting

- **No Audio Input Detected:**
  - Ensure your microphone or audio input device is properly connected and configured.
  - If using VoiceMeeter or a similar virtual audio device, make sure it is correctly set up as the input source.

- **Application Window Not Responding:**
  - Check for any errors printed to the console and ensure all dependencies are correctly installed.

- **Audio Levels Are Too High/Low:**
  - Adjust the `maxV` variable to a more suitable value for your environment.

## Additional Information

- The application uses Windows-specific APIs for certain functionalities, so it is designed to run on Windows OS. 
- For non-Windows systems, modifications might be necessary, particularly regarding window management and audio input handling.

