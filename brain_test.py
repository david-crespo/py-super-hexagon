from SimpleCV import Color, Display, Image
from Quartz.CoreGraphics import CGRectMake
import time

from brain import decide_left_or_right, get_start, find_path
from control import tap_space, press_buttons
# from parse import parse_frame
from parse2 import parse_frame
from screenshot import get_frame
from util import timer, show_img
from viz import show_frame, show_frame2, draw_grid

wh = (w, h) = 768, 480
region = CGRectMake(672, 45, w, h)

# display = Display()

print 'Go!'
tap_space()

current_pressed = None
c = 0

with timer('frame'):
    frame = Image('train/33.png')
    parsed_frame = parse_frame(frame)
    to_press = None
    if parsed_frame:
        to_press = decide_left_or_right(parsed_frame)
        print to_press
    current_pressed = to_press

    start = get_start(parsed_frame)
    path = find_path(start, 30, parsed_frame.rot_arr)

    dl = parsed_frame.rot_img.dl()
    w, h = parsed_frame.rot_img.size()

    print w
    print h

    for p in path:
        px = p[0] * w / 100
        py = h - p[1] * h / 62
        dl.rectangle((px,py), (4,4), color=Color.GREEN, filled=True)

    show_img(parsed_frame.rot_img)