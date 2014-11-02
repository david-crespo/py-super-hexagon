# credit to https://github.com/shaunlebron/super-hexagon-unwrapper
# for this code (would have probably taken me weeks to figure out otherwise)

from SimpleCV import Color, Display, Image, Line
from simplify_polygon import simplify_polygon_by_angle
from line_sample import extendToImageEdges, get_line_samples, get_angle, rotate_segment
from math import sqrt, pi
from copy import copy
from util import timer
import numpy as np

class ParsedFrame:
    """
    This holds the features that we wish to extract from a Super Hexagon frame.
    """

    def __init__(self, img, center_blob, cursor_blob, center_img):
        """
        img         = SimpleCV Image object of the original image
        center_blob = SimpleCV Blob object of the center polygon
        cursor_blob = SimpleCV Blob object of the cursor triangle
        center_img  = SimpleCV Image object used to detect center polygon
        """

        self.img = img
        self.center_img = center_img
        self.center_blob = center_blob
        self.cursor_blob = cursor_blob

        # midpoint of the center polygon
        w,h = img.size()

        # weird y-offset of center point required because I'm cutting off the
        # top of the image in order to exclude the score junk. it would be neat
        # if I could just black those sections out instead but for now I'm
        # not going to bother
        cx, cy = center_blob.centroid()
        self.center_point = (int(cx), int(cy))
        self.center_vertices = simplify_polygon_by_angle(center_blob.hull())
        self.cursor_vertices = simplify_polygon_by_angle(cursor_blob.hull())

        #######################################
        # MATRIX OF WALL STATES
        #######################################

        b = self.center_img.binarize()
        # black out the cursor and the center hexagon (vry smrt)
        b.dl().polygon(self.cursor_vertices, filled=True)
        b.dl().polygon(self.center_vertices, filled=True)

        self.b = b

        self.rot_center_vertices = []
        for p in self.center_vertices:
            self.rot_center_vertices.append(rotate_segment(self.center_point, p, pi/12))
            self.rot_center_vertices.append(rotate_segment(self.center_point, p, 3*pi/12))

        self.sight_lines = []
        for p in self.rot_center_vertices[:6]:
            l = Line(b, (self.center_point, p))
            l = extendToImageEdges(l)
            self.sight_lines.append(l)

        # sort by angle, clockwise from east
        self.sight_lines.sort(key=lambda p: get_angle(p.end_points[0], p.end_points[1]))

        half1 = []
        half2 = []
        for l in self.sight_lines:
            samples = get_line_samples(l)
            pivot = len(samples)/2

            # need to reverse the first because we want the samples from
            # the inside out
            half1.append(list(reversed(samples[:pivot])))
            half2.append(samples[pivot:])

        self.wall_states = np.array(half1 + half2)


        #######################################
        # CURSOR ANGLE
        #######################################

        # a discrete number representing angle of rotation, calculated
        # clockwise from the line to the first hexagon vertex

        self.cursor_point = map(int, cursor_blob.centroid())
        line_to_cursor = Line(center_img, (self.center_point, self.cursor_point))
        line_to_vertex = Line(center_img, (self.center_point, self.sight_lines[0].end_points[0]))
        self.cursor_angle = int(line_to_cursor.angle() - line_to_vertex.angle() + 30)

        if self.cursor_angle < 0:
            self.cursor_angle = self.cursor_angle + 360


    def draw_frame(self, layer, linecolor=Color.RED, pointcolor=Color.WHITE):
        """
        Draw the reference frame created by our detected features.
        (for debugging)

        layer = SimpleCV Image Layer object to receive the drawing operations
        """

        # Draw the cursor
        if self.cursor_vertices:
            width = 2
            layer.polygon(self.cursor_vertices, color=linecolor,width=width)

        # Draw the center polygon.
        width = 3
        # layer.polygon(self.center_vertices, color=linecolor,width=width)

        # Draw the axes by extending lines from the center past the vertices.
        c = self.center_point
        length = 100
        for p in self.center_vertices:
            p2 = (c[0] + length*(p[0]-c[0]), c[1] + length*(p[1]-c[1]))
            layer.line(c,p2,color=linecolor,width=width)

        # p1, p2 = self.sight_lines[0].end_points
        # layer.line(p1,p2,color=Color.GREEN,width=width)

        # p1, p2 = self.sight_lines[1].end_points
        # layer.line(p1,p2,color=Color.YELLOW,width=width)

        # p1, p2 = self.sight_lines[2].end_points
        # layer.line(p1,p2,color=Color.CYAN,width=width)

        for l in self.sight_lines:
            p1, p2 = l.end_points
            layer.line(p1,p2,color=Color.GREEN,width=width)

        # Draw the reference points (center and vertices)
        def circle(p):
            layer.circle(p, 10, color=linecolor, filled=True)
            layer.circle(p, 5, color=pointcolor, filled=True)
        circle(self.center_point)
        for p in self.center_vertices:
            circle(p)

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
    center_img = bg_img.erode()

    def dist(x1, y1, x2, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def is_center(b):
        max_size = h * 0.6667
        try:
            return (b.width() < max_size
                    and b.height() < max_size
                    and b.contains((midx,midy)))
        except ZeroDivisionError:
            # blob 'contains' function throws this exception for some cases.
            return false

    def is_cursor(b):
        max_size = h * 0.05 # cursor is teensy tiny
        cx, cy = b.centroid()
        max_dist_from_center = h * 0.2 # and close to the middle
        return (b.width() < max_size
                and b.height() < max_size
                and dist(cx, cy, midx, midy) < max_dist_from_center)

    # Locate the blob within a given size containing the midpoint of the screen.
    # Select the one with the largest area.
    center_blob = None
    cursor_blob = None
    blobs = center_img.binarize().findBlobs()
    if blobs:
        for b in blobs:
            if is_center(b):
                center_blob = b
                if cursor_blob: break
            elif is_cursor(b):
                cursor_blob = b
                if center_blob: break

    if center_blob and cursor_blob:
        return ParsedFrame(img, center_blob, cursor_blob, center_img)
    else:
        return None

def show_img(img):
    display = Display()
    img.show()

    # Wait for user to close the window or break out of it.
    while display.isNotDone():
        try:
            pass
        except KeyboardInterrupt:
            display.done = True
        if display.mouseRight:
            display.done = True
    display.quit()

def test():
    with timer('image'):
        img = Image('train/3.png')

    print "image size (%d, %d)" % img.size()

    with timer('parse'):
        p = parse_frame(img)

    print 'cursor angle: %d' % p.cursor_angle
    # print p.wall_states

    return p


def show_lines_on_img(p):
    # img = p.center_img.binarize()
    img = p.b
    p.draw_frame(img.dl())
    show_img(img)


def draw_grid(p):
    sl = p.wall_states.shape[0]
    N = p.wall_states.shape[1]

    chunk_w = 60
    chunk_h = 20

    img = Image((sl * chunk_w, N * chunk_h))
    dl = img.dl()

    for x in range(sl):
        for y in range(N):
            xp = x * chunk_w
            yp = (y+1)* chunk_h
            if p.wall_states[x][N - y - 1]:
                dl.rectangle((xp, yp), (chunk_w, chunk_h), color=Color.WHITE, filled=True)

    dl.circle((p.cursor_angle * 2, chunk_h * N - 5), 5, color=Color.RED, filled=True)
    show_img(img)


if __name__ == "__main__":
    p = test()
    draw_grid(p)
    # show_lines_on_img(p)
