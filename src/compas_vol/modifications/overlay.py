from compas import PRECISION


class Overlay(object):
    def __init__(self, a=None, b=None, f=0.1):
        self.a = a
        self.b = b
        self.f = f

    def __repr__(self):
        return "Overlay({0},{1},{2:.{3}f})".format(str(self.a), str(self.b), self.f, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        return da + self.f * db

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        return da + self.f * db


if __name__ == "__main__":
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere

    s = Sphere(Point(2, 3, 0), 7)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)
    f = Overlay(vs, vb, 0.2)
    print(f)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = f.get_distance((x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
