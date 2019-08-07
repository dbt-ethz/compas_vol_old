from compas.geometry import Point
from compas.geometry import Vector


class Gradient(object):
    def __init__(self, o, e=0.01):
        self.o = o
        self.e = e
        self.ex = Point(e, 0, 0)
        self.ey = Point(0, e, 0)
        self.ez = Point(0, 0, e)

    def get_gradient(self, point):
        dx = self.o.get_distance(point + self.ex) - self.o.get_distance(point + self.ex * -1)
        dy = self.o.get_distance(point + self.ey) - self.o.get_distance(point + self.ey * -1)
        dz = self.o.get_distance(point + self.ez) - self.o.get_distance(point + self.ez * -1)
        v = Vector(dx, dy, dz)
        v.unitize()
        return v


if __name__ == "__main__":
    from compas_vol.primitives import VolSphere
    from compas.geometry import Sphere

    s = Sphere(Point(1, 2, 3), 4)
    vs = VolSphere(s)

    g = Gradient(vs)
    print(vs.get_distance(Point(4, 5, 6)))
    print(g.get_gradient(Point(5, 2, 3)))
