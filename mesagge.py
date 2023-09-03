
import pyautogui as pg
import time

time.sleep(1)
for i in range(13):
    pg.write("https://youtube.com/shorts/oyjuf-rHY4k?feature=share")
    time.sleep(0.5)

    pg.press("enter")