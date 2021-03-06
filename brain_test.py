from SimpleCV import Color, Display, Image
from Quartz.CoreGraphics import CGRectMake
import time

from brain import decide_left_or_right, get_start, find_path, smooth_path
from parse import parse_frame
from screenshot import get_frame
from util import timer, show_img
from viz import show_frame, show_frame2, draw_grid

wh = (w, h) = 768, 480
region = CGRectMake(672, 45, w, h)

with timer('frame'):
    frame = Image('train/12a.png')
    parsed_frame = parse_frame(frame)
    to_press = None
    if parsed_frame:
        to_press = decide_left_or_right(parsed_frame)
        print to_press
    current_pressed = to_press

    start = get_start(parsed_frame)
    path = find_path(start, 50, parsed_frame.rot_arr)
    path = smooth_path(path)

    dl = parsed_frame.rot_img.dl()
    w, h = parsed_frame.rot_img.size()

    for p in path:
        px = p[0] * w / 100
        py = h - p[1] * h / 62
        dl.rectangle((px,py), (4,4), color=Color.GREEN, filled=True)

    show_img(parsed_frame.rot_img)