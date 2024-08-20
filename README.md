
# Pygame Mouth Animation

This script uses the Pygame library to animate the mouth of an image depending on the loudness of sound from the microphone.

## Prerequisites

-   Pygame
-   Pyaudio
-   win32api
-   win32con
-   win32gui

## Usage

1.  Rename microphone to your own in AW.py:52
2.  Run the script
3.  Speak into the microphone
4.  Observe the animation of the mouth on the window
5.  Press Escape to exit the animation

## Code explanation

-   The script first initializes the Pygame window and sets it to a borderless window of size (700, 450)
-   It then gets the handle of the current active window and sets it to be layered with a transparent background
-   The script loads the images of the character, the open mouth, and the closed mouth
-   In the main animation loop, the script checks the loudness of the sound and updates the animation accordingly
-   The script also checks for the escape key being pressed to exit the animation
-   The animation window is updated continuously

You can change the loudness threshold and the images path to your preference.

## Conclusion

This script demonstrates how to use Pygame to create a simple animation in response to sound input. It can be used as a starting point for more complex animations or interactive projects.
