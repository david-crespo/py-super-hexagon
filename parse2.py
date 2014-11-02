# an alternative approach

from SimpleCV import Color, Display, Image, Line
from simplify_polygon import simplify_polygon_by_angle
from util import dist, show_img
from copy import copy
from util import timer
import numpy as np


class ParsedFrame:
    def __init__(self, img, bimg, arr, cursor_angle):
        w,h = img.size()

        self.img = img
        self.center_point = (w/2, h/2)
        self.bimg = bimg
        self.arr = arr
        self.cursor_angle = cursor_angle


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
        line_to_cursor = Line(img, ((midx, midy), cursor_point))
        cursor_angle = line_to_cursor.angle()

        cursor_dist = dist(midx, midy, cursor_point[0], cursor_point[1])

        bimg = black_out_center(bimg, cursor_dist).applyLayers()

        arr = bimg.resize(100).getGrayNumpy() > 100

        return ParsedFrame(img, bimg, arr, cursor_angle)
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
        img = Image('train/2.png')

    print "image size (%d, %d)" % img.size()

    with timer('parse'):
        p = parse_frame(img)
        print '--------------'

    return p


if __name__ == "__main__":
    p = test()
    show_img(p.bimg)