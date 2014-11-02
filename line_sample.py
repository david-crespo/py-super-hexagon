# this is straight out of meanColor() in
# https://github.com/sightmachine/SimpleCV/blob/master/SimpleCV/Features/Detection.py

import numpy as np
from SimpleCV import Line

def get_line_samples(line, N=30):
    """
    **SUMMARY**
    Returns the mean color of pixels under the line.  Note that when the line falls "between" pixels, each pixels color contributes to the weighted average.
    **RETURNS**
    Returns an RGB triplet corresponding to the mean color of the feature.
    **EXAMPLE**
    >>> img = Image("lenna")
    >>> l = img.findLines()
    >>> c = l[0].meanColor()
    """
    (pt1, pt2) = line.end_points
    #we're going to walk the line, and take the mean color from all the px
    #points -- there's probably a much more optimal way to do this
    (maxx,minx,maxy,miny) = line.extents()

    d_x = maxx - minx
    d_y = maxy - miny
    #orient the line so it is going in the positive direction

    #if it's a straight one, we can just get mean color on the slice
    if (d_x == 0.0):
        return line.image[pt1[0]:pt1[0] + 1, miny:maxy].meanColor()
    if (d_y == 0.0):
        return line.image[minx:maxx, pt1[1]:pt1[1] + 1].meanColor()

    error = 0.0
    d_err = d_y / d_x  #this is how much our "error" will increase in every step
    px = []
    weights = []
    if (d_err < 1):
        y = miny
        #iterate over X
        for x in range(minx, maxx):
            #this is the pixel we would draw on, check the color at that px
            #weight is reduced from 1.0 by the abs amount of error
            px.append(line.image[x, y])
            weights.append(1.0 - abs(error))

            #if we have error in either direction, we're going to use the px
            #above or below
            if (error > 0): #
                px.append(line.image[x, y+1])
                weights.append(error)

            if (error < 0):
                px.append(line.image[x, y-1])
                weights.append(abs(error))

            error = error + d_err
            if (error >= 0.5):
                y = y + 1
                error = error - 1.0
    else:
        #this is a "steep" line, so we iterate over X
        #copy and paste.  Ugh, sorry.
        x = minx
        for y in range(miny, maxy):
            #this is the pixel we would draw on, check the color at that px
            #weight is reduced from 1.0 by the abs amount of error
            px.append(line.image[x, y])
            weights.append(1.0 - abs(error))

            #if we have error in either direction, we're going to use the px
            #above or below
            if (error > 0): #
                px.append(line.image[x + 1, y])
                weights.append(error)

            if (error < 0):
                px.append(line.image[x - 1, y])
                weights.append(abs(error))

            error = error + (1.0 / d_err) #we use the reciprocal of error
            if (error >= 0.5):
                x = x + 1
                error = error - 1.0

    #once we have iterated over every pixel in the line, we avg the weights
    clr_arr = np.array(px)
    weight_arr = np.array(weights)
    weighted_clrs = np.transpose(np.transpose(clr_arr) * weight_arr)
    #multiply each color tuple by its weight

    idx_interval = weight_arr.size / N
    samples = []
    for i in range(0, idx_interval * N, idx_interval):
        segment_clrs    = weighted_clrs[ i : i + idx_interval ]
        segment_weights = weight_arr[ i : i + idx_interval ]

        print segment_weights.size

        avg = sum(segment_clrs) / sum(segment_weights)
        avg = sum(avg) / 3
        samples.append(avg > 127.5)

    return samples

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