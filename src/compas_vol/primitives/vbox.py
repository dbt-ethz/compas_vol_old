from math import sqrt

from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation

__all__ = ['VolBox']


class VolBox(object):
    def __init__(self, box, radius=0.0):
        self._box = None
        self.box = box
        self.radius = float(radius)

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, box):
        if not isinstance(box, Box):
            raise ValueError
        self._box = box

    def get_distance(self, point):
        x, y, z = point
        # frame to frame: box to world
        T = Transformation.from_frame(self.box.frame)
        i = T.inverse()
        p = Point(x, y, z)
        p.transform(i)

        dx = abs(p.x) - (self.box.xsize / 2.0 - self.radius)
        dy = abs(p.y) - (self.box.ysize / 2.0 - self.radius)
        dz = abs(p.z) - (self.box.zsize / 2.0 - self.radius)
        inside = max(dx, max(dy, dz)) - self.radius
        dx = max(dx, 0)
        dy = max(dy, 0)
        dz = max(dz, 0)
        if inside + self.radius < 0:
            return inside
        else:
            corner = sqrt(dx * dx + dy * dy + dz * dz) - self.radius
            return corner


if __name__ == "__main__":
    box = Box(Frame(Point(3, 2, 0), [1, 0.2, 0.1], [-0.1, 1, 0.1]), 25, 20, 15)
    vb = VolBox(box, 5.0)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = vb.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
