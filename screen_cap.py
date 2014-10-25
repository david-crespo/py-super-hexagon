import os
from datetime import datetime
import Quartz.CoreGraphics as CG

total_time = 0
num_shots = 20

for i in range(num_shots):

    start = datetime.now()
    # os.system("screencapture -x -c screens/%d.png" % i)
    image = CG.CGWindowListCreateImage(CG.CGRectInfinite, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
    end = datetime.now()
    seconds = (end - start).total_seconds()
    print 'screen %d took %1.3f seconds' % (i, seconds)
    total_time += seconds


print 'average screenshot time: %1.3f' % (total_time/num_shots)