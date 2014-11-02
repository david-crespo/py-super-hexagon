# this is straight out of meanColor() in
# https://github.com/sightmachine/SimpleCV/blob/master/SimpleCV/Features/Detection.py

import numpy as np
from math import sin, cos, atan2, pi
from SimpleCV import Line

count = 1

def get_line_samples(line, N=40):
    global count
    # walk the line, thresholding the value on N chunks of length L/N

    (pt1, pt2) = line.end_points
    #we're going to walk the line, and take the mean color from all the px
    #points -- there's probably a much more optimal way to do this

    print '-----------'
    print line.end_points
    print '-----------'

    (minx, miny) = pt1
    (maxx, maxy) = pt2

    d_x = maxx - minx
    d_y = maxy - miny
    #orient the line so it is going in the positive direction

    px = []
    if abs(d_x) > abs(d_y):
        d = float(d_y) / d_x
        y = miny
        step = 1 if minx < maxx else -1
        for x in range(minx, maxx, step):
            pixel = line.image[x, int(y)]
            print ('(%d, %d) -- ' + str(pixel)) % (x, int(y))
            px.append(pixel)
            y += d
    else:
        d = float(d_x) / d_y
        x = minx
        step = 1 if miny < maxy else -1
        for y in range(miny, maxy, step):
            pixel = line.image[int(x), y]
            print ('(%d, %d) -- ' + str(pixel)) % (x, int(y))
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
        # if avg > 30: print avg
        samples.append(avg > 180)
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

def extendToImageEdges(line):
        """
        **SUMMARY**

        Returns the line with endpoints on edges of image.
        **RETURNS**
        Returns a :py:class:`Line` object. If line does not lies entirely inside image then returns None.
        **EXAMPLE**
        >>> img = Image("lenna")
        >>> l = Line(img, ((50, 150), (2, 225))
        >>> cr_l = l.extendToImageEdges()
        """
        pt1, pt2 = line.end_points
        pt1, pt2 = min(pt1, pt2), max(pt1, pt2)
        x1, y1 = pt1
        x2, y2 = pt2
        w, h = line.image.width-1, line.image.height-1

        if line.end_points[1][0] - line.end_points[0][0] == 0:
            slope = float("inf")
        else:
            slope = float(line.end_points[1][1] - line.end_points[0][1])/float(line.end_points[1][0] - line.end_points[0][0])

        if not 0 <= x1 <= w or not 0 <= x2 <= w or not 0 <= y1 <= w or not 0 <= y2 <= w:
            logger.warning("At first the line should be cropped")
            return None

        ep = []
        if slope == float('inf'):
            if 0 <= x1 <= w and 0 <= x2 <= w:
                return Line(line.image, ((x1, 0), (x2, h)))
        elif slope == 0:
            if 0 <= y1 <= w and 0 <= y2 <= w:
                return Line(line.image, ((0, y1), (w, y2)))
        else:
            x = (slope*x1 - y1)/slope   # top edge y = 0
            if 0 <= x <= w:
                ep.append((int(round(x)), 0))

            x = (slope*x1 + h - y1)/slope   # bottom edge y = h
            if 0 <= x <= w:
                ep.append((int(round(x)), h))

            y = -slope*x1 + y1  # left edge x = 0
            if 0 <= y <= h:
                ep.append( (0, (int(round(y)))) )

            y = slope*(w - x1) + y1 # right edge x = w
            if 0 <= y <= h:
                ep.append( (w, (int(round(y)))) )

        ep = list(set(ep))  # remove duplicates of points if line cross image at corners
        ep.sort()

        return Line(line.image, ep)