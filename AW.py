import pygame as py
import win32api
import win32con
import win32gui
import pyaudio
import audioop

def get_loudness():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    data = stream.read(1024)
    loudness = audioop.rms(data, 2)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return loudness
py.init() 
# initialize the pygame window
window_screen = py.display.set_mode((700, 450),py.NOFRAME)
# for borderless window use pygame.Noframe
# size of the pygame window will be of width 700 and height 450
hwnd = py.display.get_wm_info()["window"]
# Getting information of the current active window
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                       hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)
character = py.image.load("Sprites/head.png")
mouthO = py.image.load("Sprites/open.png")
mouthC = py.image.load("Sprites/close.png")
done = 0
while not done:  
    # Accessing the event if any occurred
    for event in py.event.get():   
        # Checking if quit button is pressed or not
        if event.type == py.QUIT:  
            #  If quit then store true
            done = 1               
        # Checking if the escape button is pressed or not
        if event.type == py.KEYDOWN:   
            # If the escape button  is pressed then store true in the variable
            if event.key == py.K_ESCAPE: 
                done = 1
     # Transparent background
    window_screen.fill((255,0,128)) 
    #  Calling the show_text function
    window_screen.blit(character, (50, 50))
    loudness = get_loudness()
    print(loudness)
    if loudness > 1000:
        window_screen.blit(mouthO, (50, 50))
        mouthC.set_alpha(0)
        mouthO.set_alpha(255)
    else:
        window_screen.blit(mouthC, (50, 50))
        mouthC.set_alpha(255)
        mouthO.set_alpha(0)
        
    py.display.update()