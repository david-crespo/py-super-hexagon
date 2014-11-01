import time
from pykeyboard import PyKeyboard

k = PyKeyboard()

def tap_space():
    k.press_key(' ')
    time.sleep(0.05)
    k.release_key(' ')

def press_left():
    k.press_key('a')

def release_left():
    k.release_key('a')

def press_right():
    k.press_key('d')

def release_right():
    k.release_key('d')

if __name__ == '__main__':
    for i in range(1, 4):
        print '%d...' % i
        time.sleep(1)

    print 'starting...'
    tap_space()

    time.sleep(1)

    print 'PRESSING UP'
    press_left()

    time.sleep(0.5)

    print 'letting go...'
    release_left()