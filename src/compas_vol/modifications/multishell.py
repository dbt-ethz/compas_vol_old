from compas import PRECISION


class MultiShell(object):

    def __init__(self, obj, thickness=1.0, distance=3.0):
        self.o = obj
        self.thickness = thickness
        self.distance = distance

    def __repr__(self):
        return 'MultiShell({0},{1:.{3}f},{2:.{3}f})'.format(str(self.o), self.thickness, self.distance, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        do = self.o.get_distance(point)
        remainder = do % self.distance
        d = min(remainder, self.distance - remainder)
        return d - self.thickness / 2

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        do = self.o.get_distance_numpy(x, y, z)
        remainder = do % self.distance
        d = np.minimum.reduce([remainder, remainder*-1 + self.distance])
        return d - self.thickness / 2


if __name__ == "__main__":
    from compas_vol.combinations import Union
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere
    import numpy as np
    import matplotlib.pyplot as plt

    s = Sphere(Point(5, 6, 0), 7)
    b = Box(Frame.worldXY(), 15, 10, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)

    u = Union(vs, vb)
    sh = MultiShell(u, 1.0, 2.5)

    x, y, z = np.ogrid[-15:15:60j, -15:15:60j, -15:15:60j]
    dm = sh.get_distance_numpy(x,y,z)
    plt.imshow(dm[:, :, 20], cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = sh.get_distance(Point(x*0.5, y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)
