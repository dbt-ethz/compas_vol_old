from compas.geometry import Point
from compas.geometry import Sphere


class VolSphere(object):
    def __init__(self, sphere):
        self.sphere = sphere

    def get_distance(self, point):
        d = point.distance_to_point(self.sphere.center)
        return d - self.sphere.radius


if __name__ == "__main__":
    o = VolSphere(Sphere(Point(4, 2, 0), 8.5))

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = o.get_distance(Point(x * 0.5, 0, -y))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
