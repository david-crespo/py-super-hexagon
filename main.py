from SimpleCV import Display
from Quartz.CoreGraphics import CGRectMake
import time

from brain import decide_left_or_right
from control import tap_space, press_buttons
# from parse import parse_frame
from parse2 import parse_frame
from screenshot import get_frame
from viz import show_frame, show_frame2, draw_grid

wh = (w, h) = 768, 480
region = CGRectMake(672, 45, w, h)

display = Display()

for i in range(3): # count to three
    print '%d...' % (i+1)
    time.sleep(1)

print 'Go!'
tap_space()

current_pressed = None
c = 0
while True:
    frame = get_frame(region)
    parsed_frame = parse_frame(frame)
    if parsed_frame:
        frame.save('frames/' + str(c) + '.png')
        c += 1

    show_frame2(display, parsed_frame, frame)
    to_press = decide_left_or_right(parsed_frame)
    press_buttons(current_pressed, to_press)
    current_pressed = to_press
