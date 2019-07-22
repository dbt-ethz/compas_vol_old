class Union(object):
    def __init__(self, a=None, b=None):
        if type(a) == list:
            self.objs = a
        else:
            self.objs = [a, b]

    def get_distance(self, point):
        ds = [o.get_distance(point) for o in self.objs]
        return min(ds)

    def get_distance_numpy(self, x, y, z):
        import numpy as np

        # da = self.objs[0].get_distance_numpy(x, y, z)
        # db = self.objs[1].get_distance_numpy(x, y, z)
        # return np.minimum(da, db)

        distances = ([o.get_distance_numpy(x, y, z) for o in self.objs])
        return np.minimum.reduce((distances))
        # alternative:
        # d = np.asarray([o.get_distance_numpy(x, y, z) for o in self.objs]).min(axis=0)

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere

    s = Sphere(Point(5, 6, 0), 9)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)
    u = Union(vs, vb)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
