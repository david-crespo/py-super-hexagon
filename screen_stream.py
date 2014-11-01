from SimpleCV import Camera, Color, Display, Image
from parse import show_img, parse_frame
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
    path = 'frame.tiff'
    w, h = 768, 480
    region = CG.CGRectMake(672, 45, w, h)
    display = Display((w, h))
    while True:
        with timer('shoot'):
            screenshot(path, region=region)

        with timer('read '):
            img = Image(path)

        with timer('parse'):
            p = parse_frame(img)

        with timer('draw '):
            if p and p.center_img:
                img2 = p.center_img.binarize()
                p.draw_frame(img2.dl())
                img2.save(display)
            else:
                img.save(display)

        print ''
