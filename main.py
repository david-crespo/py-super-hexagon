from brain import decide_action
from control import tap_space, press_buttons
from parse import parse_frame
from screenshot import screenshot

from SimpleCV import Display, Image
from Quartz.CoreGraphics import CGRectMake

import contextlib
import time

@contextlib.contextmanager
def timer(msg):
    start = time.time()
    yield
    end = time.time()
    print "%s: %.02fms" % (msg, (end-start)*1000)

tmp_frame_path = 'frame.tiff'
w, h = 768, 480
region = CGRectMake(672, 45, w, h)

def get_frame():
    with timer('shoot'):
        screenshot(tmp_frame_path, region=region)
    with timer('read '):
        frame = Image(tmp_frame_path)
    return frame

if __name__ == '__main__':
    # display = Display((w, h))
    current_pressed = None
    while True:
        frame = get_img(path)
        parsed_frame = parse_frame(frame)
        to_press = decide_left_or_right(parsed_frame)
        press_buttons(current_pressed, to_press)
