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

    def get_distance_numpy(self, x, y, z):
        import numpy as np
        from compas.geometry import matrix_from_frame

        m = matrix_from_frame(self.box.frame)
        print(m)

        dx = np.abs(x-self.box.frame.point.x) - (self.box.xsize / 2.0 - self.radius)
        dy = np.abs(y-self.box.frame.point.y) - (self.box.ysize / 2.0 - self.radius)
        dz = np.abs(z-self.box.frame.point.z) - (self.box.zsize / 2.0 - self.radius)
        inside = np.maximum(dx, np.maximum(dy, dz)) - self.radius
        dx = np.maximum(dx, 0)
        dy = np.maximum(dy, 0)
        dz = np.maximum(dz, 0)

        out = np.where((inside + self.radius) < 0, inside,
                       np.sqrt(dx**2 + dy**2 + dz**2) - self.radius)
        return out


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    box = Box(Frame(Point(3, 2, 0), [1, 0.2, 0.1], [-0.1, 1, 0.1]), 15, 10, 15)
    vb = VolBox(box, 3.0)

    x, y, z = np.ogrid[-15:15:50j, -15:15:50j, -15:15:50j]
    d = vb.get_distance_numpy(x, y, z)
    plt.imshow(abs(d[:, :, 25].T), cmap='RdBu') # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = vb.get_distance((x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '·'
    #     print(s)
