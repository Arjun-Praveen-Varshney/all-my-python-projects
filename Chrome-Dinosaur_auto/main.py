import pyautogui
from PIL import Image, ImageGrab
# from numpy import asarray
import time

def hit(key):
    pyautogui.keyDown(key)
    return

def isCollide(data):
    for i in range(270, 300):
        for j in range(300, 398):
            if data[i, j] < 100:
                hit('down')
                return 
    for i in range(270, 370):
        for j in range(398, 490):
            if data[i, j] < 100:
                hit('up')
                return 
    return 

if __name__=='__main__':
    time.sleep(2)
    # hit('up')
    while True:
        image = ImageGrab.grab().convert('L')
        data = image.load()
        isCollide(data)
        # for i in range(270, 370):
        #     for j in range(398, 490):
        #         data[i, j] = 0
        # for i in range(270, 300):
        #     for j in range(300, 398):
        #         data[i, j] = 171

        # image.show()
        # break