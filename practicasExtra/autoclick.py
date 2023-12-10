import pyautogui
import time

def autoclick(x, y, clicks, interval):
    for _ in range(clicks):
        pyautogui.click(x, y)
        time.sleep(interval)

x = 300 # Coordenada x del mouse
y = 400 # Coordenada y del mouse
clicks = 5000000000000 # Número de clics
interval = 1 # Intervalo de tiempo entre clics

autoclick(x, y, clicks, interval)