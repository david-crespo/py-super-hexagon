from SimpleCV import Display
from Quartz.CoreGraphics import CGRectMake
import time

from brain import decide_left_or_right
from control import tap_space, press_buttons
from parse import parse_frame
from screenshot import get_frame
from viz import show_frame

wh = (w, h) = 768, 440
region = CGRectMake(672, 85, w, h)

display = Display(wh)

for i in range(3): # count to three
    print '%d...' % (i+1)
    time.sleep(1)

print 'Go!'
tap_space()

current_pressed = None
while True:
    frame = get_frame(region)
    parsed_frame = parse_frame(frame)
    show_frame(display, parsed_frame, frame)
    to_press = decide_left_or_right(parsed_frame)
    press_buttons(current_pressed, to_press)
    current_pressed = to_press
