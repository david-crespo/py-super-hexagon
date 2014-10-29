from SimpleCV import Camera, Color, Display, Image
from parse import show_img


def find_markers(img):
    blobs = img.binarize().findBlobs()
    markers = [b for b in blobs if b.isCircle(tolerance=0.20)]
    return markers


if __name__ == "__main__":
    img = Image('vid_test2.png')
    # markers = find_markers(img)
    # print len(markers)
    img2 = img.colorDistance(color=(174, 255, 216)).invert().binarize()

    markers = find_markers(img2)
    print '%d circles' % len(markers)

    layer = img2.dl()
    for c in markers:
        x, y = c.centroid()
        x, y = int(x), int(y)
        layer.circle((x,y), 10, color=Color.RED, filled=True)

    show_img(img2)

# if __name__ == "__main__":
#     cam = Camera(0, { 'width': 640, 'height': 480 })
#     winsize = (640,480)
#     display = Display(winsize)

#     while display.isNotDone():
#         img = cam.getImage()
#         img.save(display)

#         if display.mouseLeft:
#               img.save("screenshot.png")

#     display.quit()