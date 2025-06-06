import pygame as py
import pyaudio

import win32api, win32gui
import win32.lib.win32con as win32con

import time
import numpy as np
import os
import sys
import ctypes
import json


# Размер окна
Window_Size = 300
# Повернуть персонажа в другую сторону 
Reflect = False 
# Максимальная громкость входного аудиопотока. Если будет больше, то программа установит значение громкости равное maxV.
# Запустите программу и протестируйте комфортную для вас громкость речи. Если вы не стесняетесь орать на всю квартиру(или у вас громкий микрофон)
# И в терминале громкость заметно больше 2000, то можете увеличить значение maxV. 
maxV=2000
BackgroundNoise=100  # Уровень шума окружения. 
# Вывод в консоль. Если хотите убрать консоль, то установите в False
DebugMode = True
ChromaKeyColor = (10, 10, 10) # (0, 255, 0) Абослютно зеленный хромокей.
Hide_character = False # Установите True, если хотите скрыть окно с персонажем. (Может быть полезно для захвата через OBS именно окна).
# Папка со спрайтами персонажа. Имена файлов должны легко сортироваться, чтобы при их упорядочивании они совпадали с вашими ожиданиями.
# Чем больше цифра в имени файла, тем больше степень открытости рта, и т.д.
sprite_folder = "Sprites"

def hide_console():
    # Получаем дескриптор текущего консольного окна
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        # Скрываем окно консоли
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE

def show_console():
    # Получаем дескриптор текущего консольного окна
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        # Показываем окно консоли
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 = SW_SHOW


if DebugMode == False:
    hide_console()

def LogLine(PrintLoudness=True, PrintSettings=False, PrintDeviceInfo=True):
    global Window_Size, Reflect
    global loudness, maxV, DebugMode
    if DebugMode == True:
        if PrintLoudness:
            print(f"Уровень громкости аудиопотока: {loudness}", end="")
            if loudness>maxV:
                print(f" Урезан как: {maxV}", end="")
            print()
        if PrintSettings:
            print(f"Установленны настройки: Размер окна: {Window_Size}, Поворот персонажа: {Reflect}, Верхний порог громкости {maxV}")
        if PrintDeviceInfo:
            json_string = json.dumps(device_info, indent=4)  
            print(json_string)
            
        print("="*100)

def Exit(p, stream):
    print("Остановка программы")
    if stream != None:
        stream.stop_stream()
        stream.close()
    p.terminate()
    py.quit()
    sys.exit(1)


def move_window():
    hwnd = py.display.get_wm_info()["window"]
    # Получаем текущую позицию курсора на экране
    x, y = win32api.GetCursorPos()
    # Перемещаем окно по координатам курсора
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x-int(Window_Size/2), y-int(Window_Size/2), 0, 0, win32con.SWP_NOSIZE)
    

def get_loudness(stream):
  
    data = stream.read(1024*3)
    numpy_data = np.frombuffer(data, dtype=np.int16)
    volume = np.abs(numpy_data).mean()
    return volume

py.init() 

# Инициализация PyGame и создание окна без рамки\ppy.init()
window_screen = py.display.set_mode((Window_Size, Window_Size), py.NOFRAME)

# Получаем hwnd и включаем слой с цветовым ключом
hwnd = py.display.get_wm_info()["window"]
win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
)
# Устанавливаем цветовой ключ для оконного слоя
win32gui.SetLayeredWindowAttributes(
    hwnd,
    win32api.RGB(*ChromaKeyColor),
    0,
    win32con.LWA_COLORKEY
)

if Hide_character:
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)



# Поддерживаемые форматы изображений
supported_formats = {".bmp", ".jpg", ".jpeg", ".png", ".gif"}

# Получаем список файлов в директории и сортируем их по имени
sprite_files = sorted([f for f in os.listdir(sprite_folder) if os.path.splitext(f)[1].lower() in supported_formats])
# Загружаем и масштабируем изображения
mouth = [py.transform.scale(py.image.load(os.path.join(sprite_folder, file)), (Window_Size, Window_Size)) for file in sprite_files]
# Поворачиваем картинки. Для изменения инвертируйте Reflect.
mouth = [py.transform.flip(picture, Reflect, False) for picture in mouth]


close = 0

p = pyaudio.PyAudio()

# Настройки аудипотока. 
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

# Звуковой поток (микрофон или другой источник через VoiceMeeter).
# Для работы с уже записанными файлами (видео или музыка), настройте VoiceMeeter.
# В настройках звука отключите реальный микрофон и включите VoiceMeeter Output и VoiceMeeter Input. 
# После настройки VoiceMeeter просто запустите воспроизведение любого медиафайла.
device_info={}

# Заливаем фон хрома-кеем и рисуем начальный кадр
window_screen.fill(ChromaKeyColor)
window_screen.blit(mouth[0], (0, 0))
py.display.update()

# Понял, что должно работать с ЛЮБЫМ микрофоном по умолчанию. 
try:
    

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    t=time.time()
    
    while not close:
        for event in py.event.get():
            if event.type == py.QUIT:
                close = True
                Exit(p, stream)
            elif event.type == py.MOUSEBUTTONDOWN:
                
                while py.mouse.get_pressed()[0]==True:
                    #print(py.mouse.get_pressed()[0])
                    py.event.pump()
                    # При нажатии на картинку вызываем функцию перемещения окна за мышью
                    move_window()
        
        loudness = get_loudness(stream) - BackgroundNoise

        LogLine(True, False, False) # Вывод информации о громкости. 

        if(loudness>maxV):
            loudness=maxV
        elif(loudness<0):
            loudness=0
        
        idx = round(loudness / maxV * (len(mouth) - 1))

        # Рисуем текущий спрайт на фоне хрома-кея
        window_screen.fill(ChromaKeyColor)
        window_screen.blit(mouth[idx], (0, 0))
        py.display.update()
        
    Exit(p, stream) 

except Exception:
    show_console()
    e = sys.exc_info()[1]
    if(e.args[0]==-9996):
        print("У вас нет микрофона или он отключен в настройках звука.")
        print("Если хотите использовать VoiceMeeter, то включите VoiceMeeter Output и VoiceMeeter Input в настройках звука.")
        print("Аудиопоток идет с устройства ввода по умолчанию. Можно настроить в настройках звука")
    elif(e.args[0]==-9998):
        print(f"Убедитесь, что количество каналов в настройках микрофона/VoiceMeeter не меньше, чем значение CHANNELS. Сейчас у вас CHANNELS = {CHANNELS}")
    else:
        print(e)
    input("Нажмите Enter")
    Exit(p, stream=None)
