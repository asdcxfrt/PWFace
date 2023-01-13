
# Pygame Mouth Animation

This script uses the Pygame library to animate the mouth of an image depending on the loudness of sound from the microphone.

[![Demonstration of work](http://img.youtube.com/vi/dA99VW8Em7U/0.jpg)](http://www.youtube.com/watch?v=dA99VW8Em7U "Demonstration of work")

## Prerequisites

-   Pygame
-   Pyaudio
-   win32api
-   win32con
-   win32gui

## Usage

1.  Run the script
2.  Speak into the microphone
3.  Observe the animation of the mouth on the window
4.  Press Escape to exit the animation

## Code explanation

-   The script first initializes the Pygame window and sets it to a borderless window of size (700, 450)
-   It then gets the handle of the current active window and sets it to be layered with a transparent background
-   The script loads the images of the character, the open mouth, and the closed mouth
-   In the main animation loop, the script checks the loudness of the sound and updates the animation accordingly
-   The script also checks for the escape key being pressed to exit the animation
-   The animation window is updated continuously

You can change the loudness threshold and the images path to your preference.

## Note

The script uses the win32api and win32con library to set the window to always be on top of other windows. This feature could be annoying for the user, so it's recommended to use it sparingly and only when it's necessary for the functionality of your program.

## Conclusion

This script demonstrates how to use Pygame to create a simple animation in response to sound input. It can be used as a starting point for more complex animations or interactive projects.
