from compas.geometry._primitives import Box, Frame, Point
from compas.geometry.xforms import Transformation
from math import sqrt

class VolBox(object):
    def __init__(self, frame=Frame.worldXY(), xsize=3.0, ysize=2.0, zsize=1.0, rad=0.0):
        self._cbox = None
        self.cbox = Box(frame, xsize, ysize, zsize)
        self._r = rad
    
    @property
    def cbox(self):
        return self._cbox

    @cbox.setter
    def cbox(self,cb):
        self._cbox = cb
    
    def get_distance(self,x,y,z):
        T = Transformation.from_frame(self.cbox.frame)
        i = T.inverse()
        p = Point(x,y,z)
        p.transform(i)

        dx = abs(p.x) - (self.cbox.xsize/2.0 - self._r)
        dy = abs(p.y) - (self.cbox.ysize/2.0 - self._r)
        dz = abs(p.z) - (self.cbox.zsize/2.0 - self._r)
        inside = max(dx, max(dy,dz)) - self._r
        dx = max(dx,0)
        dy = max(dy,0)
        dz = max(dz,0)
        if inside+self._r<0:
            return inside
        else:
            corner = sqrt(dx*dx + dy*dy + dz*dz) - self._r
            return corner

if __name__ == "__main__":
    vb = VolBox(Frame(Point(3,2,0),[1,0.2,0.1],[-0.1,1,0.1]),25,20,15,5.0)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = vb.get_distance(x*0.5,-y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)
