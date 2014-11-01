from SimpleCV import Image, Display
from screenshot import screenshot
import Quartz.CoreGraphics as CG

import contextlib
import time

@contextlib.contextmanager
def timer(msg):
    start = time.time()
    yield
    end = time.time()
    print "%s: %.02fms" % (msg, (end-start)*1000)

if __name__ == '__main__':
    path = 'test/tmp.png'
    region = CG.CGRectMake(0, 0, 800, 600)
    # display = Display((800,600))
    while True:
        with timer('shot'):
            screenshot(path)
            img = Image(path)
            # img.save(display)