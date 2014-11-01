import Quartz
import LaunchServices
from Cocoa import NSURL
import Quartz.CoreGraphics as CG
from SimpleCV import Image

# credit to https://github.com/troq/flappy-bird-player for this code

tmp_frame_path = 'frame.tiff'

def get_frame(region=None):
    screenshot(tmp_frame_path, region=region)
    return Image(tmp_frame_path)


def screenshot(path, region=None):
    """saves screenshot of given region to path
    :path: string path to save to
    :region: tuple of (x, y, width, height)
    :returns: nothing
    """
    if region is None:
        region = CG.CGRectInfinite

    # Create screenshot as CGImage
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)

    dpi = 72 # FIXME: Should query this from somewhere, e.g for retina displays

    url = NSURL.fileURLWithPath_(path)

    dest = Quartz.CGImageDestinationCreateWithURL(url, LaunchServices.kUTTypeTIFF, 1, None)

    properties = {
        Quartz.kCGImagePropertyDPIWidth: dpi,
        Quartz.kCGImagePropertyDPIHeight: dpi,
    }

    # Add the image to the destination, characterizing the image with
    # the properties dictionary.
    Quartz.CGImageDestinationAddImage(dest, image, properties)

    # When all the images (only 1 in this example) are added to the destination,
    # finalize the CGImageDestination object.
    Quartz.CGImageDestinationFinalize(dest)