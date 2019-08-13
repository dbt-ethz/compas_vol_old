from math import sqrt

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Torus
from compas.geometry import distance_point_point_xy
from compas.geometry import inverse
from compas.geometry import matrix_from_frame

__all__ = ['VolTorus']


class VolTorus(object):
    """A volumetric torus is defined by a base torus from `compas.geometry`.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        The base torus.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> from compas_vol.primitives import VolTorus
    >>> ctorus = Torus(Plane.worldXY(), 5., 2.)
    >>> vtorus = VolTorus(ct)
    """
    def __init__(self, torus):
        self.torus = torus

    def get_distance(self, point):
        """
        point by point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)

        frame = Frame.from_plane(self.torus.plane)
        m = matrix_from_frame(frame)
        mi = inverse(m)
        point.transform(mi)

        dxy = distance_point_point_xy(self.torus.center, point)
        d2 = sqrt((dxy - self.torus.radius_axis)**2 + point.z**2)
        return d2 - self.torus.radius_pipe

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        frame = Frame.from_plane(self.torus.plane)
        m = matrix_from_frame(frame)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)

        d = np.sqrt((xt - self.torus.center.x)**2 +
                    (yt - self.torus.center.y)**2) - self.torus.radius_axis
        d2 = np.sqrt(d**2 + (zt - self.torus.center.z)**2)
        return d2 - self.torus.radius_pipe


if __name__ == "__main__":
    from compas.geometry import Plane
    import matplotlib.pyplot as plt
    import numpy as np

    o = VolTorus(Torus(Plane((0, 0, 0), (0.3, 0.2, 1)), 7.0, 4.0))

    x, y, z = np.ogrid[-13:13:60j, -13:13:60j, -13:13:60j]
    d = o.get_distance_numpy(x, y, z)
    plt.imshow(d[:, :, 30], cmap='RdBu')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = o.get_distance(Point(x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '·'
    #     print(s)
