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
    w, h = 768, 480
    region = CG.CGRectMake(672, 45, w, h)
    display = Display((w, h))
    while True:
        with timer('shot'):
            screenshot(path, region=region)
            img = Image(path)
            img.save(display)