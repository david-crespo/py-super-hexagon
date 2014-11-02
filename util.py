from SimpleCV import Display

from math import sqrt, atan2
from cmath import polar, rect
import contextlib
import time

@contextlib.contextmanager
def timer(msg):
    start = time.time()
    yield
    end = time.time()
    print "%s: %.02fms" % (msg, (end-start)*1000)

def show_img(img):
    display = Display()
    img.show()

    # Wait for user to close the window or break out of it.
    while display.isNotDone():
        try:
            pass
        except KeyboardInterrupt:
            display.done = True
        if display.mouseRight:
            display.done = True
    display.quit()

def dist(x1, y1, x2, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

def cart_to_polar(x,y):
    return sqrt(x*x + y*y), atan2(y, x)
