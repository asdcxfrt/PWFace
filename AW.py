import pygame as py
import win32api
import win32con
import win32gui
import pyaudio
import audioop
import math
import time
import numpy as np

def move_window():
    hwnd = py.display.get_wm_info()["window"]
    # Получаем текущую позицию курсора на экране
    x, y = win32api.GetCursorPos()
    # Перемещаем окно по координатам курсора
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x-350, y-350, 0, 0, win32con.SWP_NOSIZE)
    

def get_loudness(stream):
  
    data = stream.read(1024*3)
    numpy_data = np.frombuffer(data, dtype=np.int16)
    volume = np.abs(numpy_data).mean()
    return volume

py.init() 

window_screen = py.display.set_mode((700, 700),py.NOFRAME)
hwnd = py.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                       hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)

character = py.image.load("Sprites/PWGood1.png")
mouth5 = py.image.load("Sprites/PWGood6.png")
mouth4 = py.image.load("Sprites/PWGood5.png")
mouth3 = py.image.load("Sprites/PWGood4.png")
mouth2 = py.image.load("Sprites/PWGood3.png")
mouth1 = py.image.load("Sprites/PWGood2.png")
mouth=[character,mouth1,mouth2,mouth3,mouth4,mouth5]

close = 0
countframes=0
old=0
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

device_index = None
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    #print(device_info)
    if "VoiceMeeter" in device_info["name"]:
        device_index = i
        break

if device_index is None:
    print("Не удалось найти зацикленное звуковое устройство.")
    exit()
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# создание входного потока аудио
#stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=device_index, frames_per_buffer=CHUNK_SIZE)
maxV=2000
t=time.time()
window_screen.fill((255,0,128))
window_screen.blit(character, (50, 50))
while not close:
    for event in py.event.get():
        if event.type == py.QUIT:
            close = True
        elif event.type == py.MOUSEBUTTONDOWN:
            
            while py.mouse.get_pressed()[0]==True:
                print(py.mouse.get_pressed()[0])
                py.event.get()
                # При нажатии на картинку вызываем функцию перемещения окна за мышью
                move_window()
    
    loudness = get_loudness(stream)
    print(loudness)
    if(loudness>maxV):
        loudness=maxV
    
    Number_mouth=round(loudness/maxV*5)
    print(Number_mouth)
    for i in range(0,len(mouth)):
        window_screen.blit(mouth[Number_mouth], (50, 50))
        if(Number_mouth==i):
            mouth[i].set_alpha(0)
        else:
            mouth[i].set_alpha(255)
    else:
        #time.sleep(1/10)
        py.display.update()
stream.stop_stream()
stream.close()
p.terminate()
py.quit()
