# this is straight out of meanColor() in
# https://github.com/sightmachine/SimpleCV/blob/master/SimpleCV/Features/Detection.py

import numpy as np
from math import sin, cos, atan2, pi, sqrt
from SimpleCV import Line

count = 1

def get_line_samples(line, N=20):
    global count
    # walk the line, thresholding the value on N chunks of length L/N

    (pt1, pt2) = line.end_points
    #we're going to walk the line, and take the mean color from all the px
    #points -- there's probably a much more optimal way to do this

    # print '-----------'
    # print line.end_points
    # print '-----------'

    (minx, miny) = pt1
    (maxx, maxy) = pt2

    w, h = line.image.size()

    d_x = maxx - minx
    d_y = maxy - miny
    #orient the line so it is going in the positive direction

    px = []
    if abs(d_x) > abs(d_y):
        d = abs(float(d_y) / d_x)
        if d_y < 0: d *= -1

        y = miny
        step = 1 if minx < maxx else -1
        for x in range(minx, maxx, step):
            inty = int(y)
            if 0 <= x < w and 0 <= inty < h:
                pixel = line.image[x, inty]
            else:
                pixel = (0.0,0.0,0.0)
            # if pixel != (0.0,0.0,0.0): print '(%d, %d) -- %s' % (x, inty, str(pixel))
            px.append(pixel)
            y += d
    else:
        d = abs(float(d_x) / d_y)
        if d_x < 0: d *= -1

        x = minx
        step = 1 if miny < maxy else -1
        for y in range(miny, maxy, step):
            intx = int(x)
            s = ('(%d, %d) -- ' % (intx, y))
            if 0 <= intx < w and 0 <= y < h:
                pixel = line.image[intx, y]
            else:
                pixel = (0.0,0.0,0.0)
            # if pixel != (0.0,0.0,0.0): print '(%d, %d) -- %s' % (intx, y, str(pixel))
            px.append(pixel)
            x += d

    count += 1

    #once we have iterated over every pixel in the line, we avg the weights
    clr_arr = np.array(px)
    interval = float(clr_arr.size) / 3 / N
    int_interval = int(interval)


    # print clr_arr.size / 3
    # print interval
    # print '-----------'

    samples = []
    idx = 0
    for chunk_number in range(N):
        i = int(idx)
        segment_clrs = clr_arr[ i : i + int_interval ]
        # print str(i) + '  ',
        # print segment_clrs
        avg = sum(sum(segment_clrs) / segment_clrs.size)
        # if avg > 30:
            # print avg
            # print str(i) + '  ',
            # print segment_clrs
        samples.append(avg > 130)
        idx += interval

    return samples

def get_angle(center, outer):
    y = outer[1] - center[1]
    x = outer[0] - center[0]
    return int(atan2(y,x) * 360 / (2 * pi))

def rotate_segment(center, outer, angle):
    angle = -angle ## turn it clockwise
    x, y = outer[0] - center[0], outer[1] - center[1]
    cosval, sinval = cos(angle), sin(angle)
    rot_x = x * cosval + y * sinval
    rot_y = y * cosval - x * sinval
    return (int(rot_x + center[0]), int(rot_y + center[1]))

def create_ray(img, center, point, radius):
    if point[0] == center[0]:
        sign = 1 if point[1] > center[1] else -1
        endpoint = (center[0], center[1] + sign * radius)
    else:
        slope = (float(point[1]) - center[1]) / (point[0] - center[0])

        x = sqrt(radius**2 / (1 + slope**2))
        y = abs(slope * x)

        xsign = 1 if point[0] > center[0] else -1
        ysign = 1 if point[1] > center[1] else -1

        endpoint = (int(center[0] + x * xsign), int(center[1] + y * ysign))

    return Line(img, (center, endpoint))
