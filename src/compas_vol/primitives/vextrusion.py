from compas.geometry import Point
from compas.geometry import closest_point_on_polyline_xy


class VolExtrusion(object):
    def __init__(self, polyline, height=1.0):
        self.polyline = polyline
        self.height = height

    def get_distance(self, point):
        if not isinstance(point, Point):
            point = Point(*point)
        cp = closest_point_on_polyline_xy(point, self.polyline)
        d = point.distance_to_point(cp)
        return d-2

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":
    import math
    polyline = []
    a = math.pi*2/10
    r = 10
    for i in range(10):
        tr = r
        if i % 2:
            tr = 5
        x = tr*math.cos(i*a)
        y = tr*math.sin(i*a)
        polyline.append((x, y, 0))
    polyline.append(polyline[0])

    ve = VolExtrusion(polyline)

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = ve.get_distance(Point(x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
