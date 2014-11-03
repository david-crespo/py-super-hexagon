# an alternative approach

from SimpleCV import Color, Display, Image, Line
from util import dist, show_img, timer, cart_to_polar

import PIL

import numpy as np
from math import sqrt, ceil, pi, atan2

class ParsedFrame:
    def __init__(self, img, bimg, arr, rot_arr, rot_img, cursor_r, cursor_angle):
        w,h = img.size()

        self.img = img
        self.center_point = (w/2, h/2)
        self.bimg = bimg
        self.arr = arr
        self.rot_arr = rot_arr
        self.rot_img = rot_img
        self.cursor_r = cursor_r
        self.cursor_angle = cursor_angle

        rw, rh = self.rot_img.size()

        max_r = ceil(dist(0, 0, w/2, h/2))

        cursor_y = rh - int(rh * cursor_r/max_r)
        cursor_x = int(float(rw) * self.cursor_angle / 360)

        self.rot_img.dl().circle((cursor_x, cursor_y), 3, color=Color.RED, filled=True)


def parse_frame(img):
    """
    Parses a SimpleCV image object of a frame from Super Hexagon.
    Returns a ParsedFrame object containing selected features.
    """

    # helper image size variables
    w,h = img.size()
    midx,midy = w/2,h/2

    # Create normalized images for targeting objects in the foreground or background.
    # (This normalization is handy since Super Hexagon's colors are inverted for some parts of the game)
    # fg_img = foreground image (bright walls, black when binarized)
    # bg_img = background image (bright space, black when binarized)
    fg_img = img
    if sum(img.binarize().getPixel(midx,midy)) == 0:
        fg_img = img.invert()
    bg_img = fg_img.invert()

    # Locate the CENTER blob.

    # We need to close any gaps around the center wall so we can detect its containing blob.
    # The gaps are resulting artifacts from video encoding.
    # The 'erode' function does this by expanding the dark parts of the image.
    bimg = bg_img.erode().binarize()
    bimg = black_out_GUI(bimg)

    blobs = bimg.findBlobs()
    cursor_blob = get_cursor_blob(blobs, h, midx, midy)

    if cursor_blob:
        cursor_point = map(int, cursor_blob.centroid())
        cursor_r, cursor_angle = cart_to_polar(cursor_point[0] - midx, midy - cursor_point[1])

        cursor_angle = int(cursor_angle * 360/ (2 * pi))
        cursor_angle = 180 - cursor_angle
        if cursor_angle < 0:
            a += 360

        bimg = black_out_center(bimg, cursor_r).applyLayers()
        arr = bimg.resize(100).getGrayNumpy() > 100
        rot_arr = arr_to_polar(arr)
        rot_img = Image(PIL.Image.fromarray(np.uint8(np.transpose(rot_arr)*255))).dilate()
        rot_arr = rot_img.getGrayNumpy() > 100
        rot_img = rot_img.resize(400).flipVertical()
        return ParsedFrame(img, bimg, arr, rot_arr, rot_img, cursor_r, cursor_angle)
    else:
        return None

def get_cursor_blob(blobs, h, midx, midy):
    def is_cursor(b):
        max_size = h * 0.05 # cursor is teensy tiny
        cx, cy = b.centroid()
        max_dist_from_center = h * 0.2 # and close to the middle
        return (b.width() < max_size
                and b.height() < max_size
                and dist(cx, cy, midx, midy) < max_dist_from_center)

    # Locate the blob within a given size containing the midpoint of the screen.
    # Select the one with the largest area.
    cursor_blob = None

    if blobs:
        for b in blobs:
            if is_cursor(b):
                cursor_blob = b
                break

    return cursor_blob


def arr_to_polar(arr):
    w, h = arr.shape
    cx, cy = w/2, h/2
    max_r = ceil(dist(0, 0, cx, cy))

    new_w = 100
    new_h = 62

    x_bound = new_w - 1
    y_bound = new_h - 1

    new_arr = np.zeros((new_w, new_h), dtype=np.bool_)

    it =  np.nditer(arr, flags=['multi_index'])
    while not it.finished:
        x, y = it.multi_index
        r, t = cart_to_polar(x-cx,cy-y) # flip y

        new_x = x_bound - int(x_bound * (t + pi) / ( 2 * pi))
        new_y = int(y_bound * r/max_r)

        new_arr[new_x, new_y] = it[0]
        it.iternext()

    return new_arr


def black_out_GUI(img):
    dl = img.dl()
    dl.rectangle((0,0), (209, 31), filled=True)

    total_w = img.size()[0]
    w2, h2 = (229, 31)
    w3, h3 = (111, 51)

    dl.rectangle((total_w-w2,0), (w2, h2), filled=True)
    dl.rectangle((total_w-w3,0), (w3, h3), filled=True)

    return img

def black_out_center(img, radius):
    dl = img.dl()
    w,h = img.size()
    center = (w/2, h/2)
    dl.circle(center, radius+10, filled=True)

    return img

def test():
    with timer('image'):
        img = Image('train/372.png')

    print "image size (%d, %d)" % img.size()

    with timer('parse'):
        p = parse_frame(img)
        print '--------------'

    return p


if __name__ == "__main__":
    p = test()
    if p:
        print 'cursor angle: %d' % p.cursor_angle
        show_img(p.rot_img)
    else:
        print 'PARSE FAILED'