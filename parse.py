# credit to https://github.com/shaunlebron/super-hexagon-unwrapper
# for this code (would have probably taken me weeks to figure out otherwise)

from SimpleCV import Color, Display, Image
from simplify_polygon import simplify_polygon_by_angle
from math import sqrt
from util import timer

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
        # (Just assume center of image is center point instead of using
        # center_blob.centroid())
        w,h = img.size()
        self.center_point = (w/2, h/2 - 35)

        # vertices of the center polygon
        # (remove redundant vertices)
        self.center_vertices = simplify_polygon_by_angle(center_blob.hull())

        self.cursor_vertices = None
        if cursor_blob:
            self.cursor_vertices = simplify_polygon_by_angle(cursor_blob.hull())

    def draw_frame(self, layer, linecolor=Color.RED, pointcolor=Color.WHITE):
        """
        Draw the reference frame created by our detected features.
        (for debugging)

        layer = SimpleCV Image Layer object to receive the drawing operations
        """

        # Draw the cursor
        if self.cursor_vertices:
            width = 3
            layer.polygon(self.cursor_vertices, color=linecolor,width=width)

        # Draw the center polygon.
        width = 5
        layer.polygon(self.center_vertices, color=linecolor,width=width)

        # Draw the axes by extending lines from the center past the vertices.
        c = self.center_point
        length = 100
        for p in self.center_vertices[:2]:
            p2 = (c[0] + length*(p[0]-c[0]), c[1] + length*(p[1]-c[1]))
            layer.line(c,p2,color=linecolor,width=width)

        # Draw the reference points (center and vertices)
        def circle(p):
            layer.circle(p, 10, color=linecolor, filled=True)
            layer.circle(p, 5, color=pointcolor, filled=True)
        circle(self.center_point)
        for p in self.center_vertices[:2]:
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

    if center_blob:
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
    p = parse_frame(Image('train/1.png'))
    return p


def test_line():
    from SimpleCV import Line
    from line_sample import extendToImageEdges

    p = parse_frame(Image('train/1.png'))
    b = p.center_img.binarize()
    l = Line(b, (p.center_point, p.center_vertices[1]))
    l = extendToImageEdges(l)
    return p, l


def show_lines_on_img(p):
    img = p.center_img.binarize()
    p.draw_frame(img.dl())
    show_img(img)


if __name__ == "__main__":

    # Run a test by drawing the reference frame parsed from a screenshot.
    with timer('parse frame'):
        p = parse_frame(Image('train/1.png'))
    if p:
        show_lines_on_img(p)

    # Wait for user to close the window or break out of it.
    while display.isNotDone():
        try:
            pass
        except KeyboardInterrupt:
            display.done = True
        if display.mouseRight:
            display.done = True
    display.quit()
