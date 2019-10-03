from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import is_point_in_polygon_xy


class VolExtrusion(object):
    def __init__(self, polyline, height=1.0, frame=None):
        self.polyline = polyline
        self.height = height
        self.frame = frame or Frame.worldXY()

    def get_distance(self, point):
        if not isinstance(point, Point):
            point = Point(*point)

        m = matrix_from_frame(self.frame)
        mi = matrix_inverse(m)
        point.transform(mi)

        tp = Point(point[0], point[1], 0)
        cp = closest_point_on_polyline_xy(tp, self.polyline)
        d = tp.distance_to_point(cp)
        if is_point_in_polygon_xy(tp, self.polyline):
            d = -1.*d
        d = max(d, abs(point.z) - self.height / 2.0)
        return d

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":
    import math
    import matplotlib.pyplot as plt
    import numpy as np

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

    ve = VolExtrusion(polyline, height=20, frame=Frame((1, 2, 3), (1, 0.3, 0.1), (-0.4, 1, 0.3)))

    m = np.empty((60, 30))
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = ve.get_distance(Point(x * 0.5, -y, 0))
            m[x + 30, y + 15] = d
        #     if d < 0:
        #         s += 'x'
        #     else:
        #         s += '.'
        # print(s)
    plt.imshow(m, cmap='RdBu')
    plt.colorbar()
    plt.show()
