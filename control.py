import time
from pykeyboard import PyKeyboard

k = PyKeyboard()

def press(key):
    if key == 'left':
        k.press_key('a')
    elif key == 'right':
        k.press_key('d')

def release(key):
    if key == 'left':
        k.release_key('a')
    elif key == 'right':
        k.release_key('d')

def tap_space():
    k.press_key(' ')
    time.sleep(0.05)
    k.release_key(' ')

def press_buttons(current_pressed, to_press):
    if to_press:
        if current_pressed and current_pressed != to_press:
            release(current_pressed)
        press(to_press)
    elif current_pressed:
        # i.e., if to_press is None and there's currently a key pressed
        release(current_pressed)