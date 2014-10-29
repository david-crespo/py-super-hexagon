from SimpleCV import Camera

cam = Camera(0, { 'width': 640, 'height': 480 })

while True:
    img = cam.getImage()
    img.show()