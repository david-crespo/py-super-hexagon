from a_star import find_path
from heap import Heap
from math import ceil
from util import dist

def decide_left_or_right(parsed_frame):
    '''
    based on the position of the cursor and walls, decide whether to
        1) press left (return 'left')
        2) press right (return 'right')
        3) do nothing (return None)
    '''
    action = None

    start = get_start(parsed_frame)
    path = find_path(start, 40, parsed_frame.rot_arr)

    if path and len(path) > 10:
        start_x = start[0]
        next = path[8]
        next_x  = next[0]

        min_x_jump = 0
        min_y_jump = 0

        print '-------------------'
        print 'start: (%d, %d)' % start
        print 'next:  (%d, %d)' % next

        if next[1] - start[1] >= min_y_jump:
            if start_x == 0 and next_x > 50 and next_x <= 62 - min_x_jump: # wrap around
                action = 'left'
            elif start_x == 61 and next_x >= min_x_jump and next_x < 10: # wrap around
                action = 'right'
            elif next_x > start_x + min_x_jump:
                action = 'right'
            elif next_x < start_x - min_x_jump:
                action = 'left'

    return action

def get_start(parsed_frame):
    w, h = parsed_frame.img.size()
    rw, rh = parsed_frame.rot_arr.shape
    max_r = ceil(dist(0, 0, w/2, h/2))

    cursor_x = int(float(rw) * parsed_frame.cursor_angle / 360)
    cursor_y = int(rh * parsed_frame.cursor_r/max_r)

    return cursor_x, cursor_y