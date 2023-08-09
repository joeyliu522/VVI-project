import time

from pynput.mouse import Button,Controller as mouseController
from pynput.keyboard import Listener
from pynput import keyboard as pynputkeyboard
import KeyboardMouse
mouse = mouseController()
#Keyboard Listener
cords = []
def OnPress (key):

    if key == pynputkeyboard.Key.esc:
        print(KeyboardMouse.mouse.position)
        cords.append(KeyboardMouse.mouse.position)
    if key == pynputkeyboard.Key.end:
        print("Coords:")
        print(cords)
        cords.clear()


listener = pynputkeyboard.Listener(on_press = OnPress)
listener.start()



while True:

    time.sleep(0.1)