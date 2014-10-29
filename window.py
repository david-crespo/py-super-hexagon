from SimpleCV import Camera, Display, Image

cam = Camera(0, { 'width': 640, 'height': 480 })




# def find_markers(img):

if __name__ == "__main__":
    winsize = (640,480)
    display = Display(winsize)

    while display.isNotDone():
        img = cam.getImage()
        img.save(display)

        if display.mouseLeft:
              img.save("screenshot.png")

    display.quit()