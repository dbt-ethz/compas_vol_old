from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Torus
from compas.geometry import distance_point_point_xy
from math import sqrt


__all__ = ['VolTorus']


class VolTorus(object):
    """
    here goes the doc for the donut
    """
    def __init__(self, torus):
        self.torus = torus

    def get_distance(self, point):
        if not isinstance(point, Point):
            point = Point(*point)
        dxy = distance_point_point_xy(self.torus.center, point)
        d2 = sqrt((dxy - self.torus.radius_axis)**2 + point.z**2)
        return d2 - self.torus.radius_pipe

    def get_distance_numpy(self, x, y, z):
        import numpy as np
        from compas.geometry import matrix_from_frame, inverse

        frame = Frame.from_plane(self.torus.plane)
        m = matrix_from_frame(frame)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)

        d = np.sqrt((xt - self.torus.center.x)**2 +
                    (yt - self.torus.center.y)**2)


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
