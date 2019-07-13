from compas.geometry import Point
# from compas.geometry import Torus
from compas.geometry import distance_point_point_xy
from math import sqrt


__all__ = ['VolTorus']


class VolTorus(object):
    def __init__(self, torus):
        self.torus = torus

    def get_distance(self, point):
        dxy = distance_point_point_xy(self.torus.center, point)
        d2 = sqrt((dxy - self.torus.radius_axis)**2 + point.z**2)
        return d2 - self.torus.radius_pipe


if __name__ == "__main__":
    from compas.geometry import Plane

    o = VolTorus(Torus(Plane.worldXY(), 7.0, 4.0))

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = o.get_distance(Point(x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
