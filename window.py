from SimpleCV import Camera, Color, Display, Image
from parse import show_img, parse_frame


def find_markers(img):
    blobs = img.binarize().findBlobs()
    markers = [b for b in blobs if b.isCircle(tolerance=0.20)]
    return markers


# if __name__ == "__main__":
#     img = Image('vid_test2.png')
#     # markers = find_markers(img)
#     # print len(markers)
#     img2 = img.colorDistance(color=(174, 255, 216)).invert().binarize()

#     markers = find_markers(img2)
#     print '%d circles' % len(markers)

#     layer = img2.dl()
#     for c in markers:
#         x, y = c.centroid()
#         x, y = int(x), int(y)
#         layer.circle((x,y), 10, color=Color.RED, filled=True)

#     show_img(img2)


# if __name__ == "__main__":
#     img = Image('vid_test2.png').colorDistance(color=(174, 255, 216))
#     circles = img.findCircle(canny=200,thresh=120)
#     circles.draw(color=Color.RED, width=4)
#     img2 = img.applyLayers()
#     show_img(img2)


if __name__ == "__main__":
    w = 1920
    h = 1080

    scale = 1.0

    x_offset = (1 - scale) * w
    w2 = int(w * scale)
    y_offset = (1 - scale) * h
    h2 = int(h * scale)

    cam = Camera(0, { 'width': w, 'height': h })
    display = Display((w2/3,h2/3))

    while display.isNotDone():
        img = cam.getImage() #.crop(x_offset, y_offset, w2, h2)

        p = parse_frame(img)
        if p and p.center_img:
            img2 = p.center_img.binarize()
            p.draw_frame(img2.dl())
            img2.save(display)
        else:
            img.save(display)

        # if display.mouseLeft:
        #       img.save("screenshot.png")

    display.quit()