from compas.geometry import Point
from compas.geometry import Cylinder
from compas.geometry import distance_point_point_xy


__all__ = ['VolCylinder']


class VolCylinder(object):
    def __init__(self, cylinder):
        self.cylinder = cylinder

    def get_distance(self, point):
        dxy = distance_point_point_xy(self.cylinder.center, point)
        d = dxy - self.cylinder.radius
        d = max(d, abs(point.z) - self.cylinder.height / 2.0)
        return d


if __name__ == "__main__":
    from compas.geometry import Circle, Plane

    o = VolCylinder(Cylinder(Circle(Plane.worldXY(), 5.0), 7.0))

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = o.get_distance(Point(x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
