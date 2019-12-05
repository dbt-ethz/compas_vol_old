from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
from compas import PRECISION


__all__ = ['VolEllipsoid']


class VolEllipsoid(object):
    """A volumetric sphere is defined by a base sphere from `compas.geometry`.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        The base sphere.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Sphere
    >>> from compas_vol.primitives import VolSphere
    >>> cs = Sphere(Point(1, 1, 1), 5)
    >>> vs = VolSphere(cs)
    """
    def __init__(self, radiusX=3, radiusY=2, radiusZ=1, frame=Frame.worldXY()):
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.radiusZ = radiusZ
        self.frame = frame
        transform = matrix_from_frame(self.frame)
        self.inversetransform = matrix_inverse(transform)

    def get_distance(self, point):
        if not isinstance(point, Point):
            p = Point(*point)
        else:
            p = point

        p.transform(self.inversetransform)

        k0 = Vector(p.x / self.radiusX, p.y / self.radiusY, p.z / self.radiusZ).length
        k1 = Vector(p.x / self.radiusX**2, p.y / self.radiusY**2, p.z / self.radiusZ**2).length
        return k0 * (k0 - 1.0) / max(k1, 0.000000001)

    def get_distance_numpy(self, x, y, z):
        import numpy as np

        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(self.inversetransform, p)
        k0 = np.sqrt(np.square(xt/self.radiusX) + np.square(yt/self.radiusY) + np.square(zt/self.radiusZ))
        k1 = np.sqrt(np.square(xt/self.radiusX**2) + np.square(yt/self.radiusY**2) + np.square(zt/self.radiusZ**2))
        return k0 * (k0 - 1.0) / np.maximum(k1, 0.000000001)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    e = VolEllipsoid(14, 10, 6)

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = e.get_distance(Point(x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)

    x, y, z = np.ogrid[-15:15:61j, -15:15:61j, -15:15:61j]
    d = e.get_distance_numpy(x, y, z)
    plt.imshow(d[:, :, 30]<0, cmap='RdBu')
    plt.axis('equal')
    plt.show()
