from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
from compas import PRECISION


class VolEllipsoid(object):
    """A volumetric ellipsoid is defined by three radii along its axes x, y and z.

    Parameters
    ----------
    radiusX : float
        The radius along the X axis
    radiusY : float
        The radius along the Y axis
    radiusZ : float
        The radius along the Z axis
    frame : :class:`compas.geometry.Frame`
        The base frame.

    Examples
    --------
    >>> TODO
    """

    def __init__(self, radiusX=3, radiusY=2, radiusZ=1, frame=Frame.worldXY()):
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.radiusZ = radiusZ
        self.frame = frame
        transform = matrix_from_frame(self.frame)
        self.inversetransform = matrix_inverse(transform)

    def __repr__(self):
        return 'VolEllipsoid({0:.{4}f},{1:.{4}f},{2:.{4}f},{3})'.format(self.radiusX, self.radiusY, self.radiusZ, str(self.frame), PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function

        Parameters
        ----------
        point: :class:`compas.geometry.Point`
            The point in R<sup>3</sup> space to query for it's distance.
        Returns
        -------
        float
            The distance from the query point to the surface of the object.
        """
        if not isinstance(point, Point):
            p = Point(*point)
        else:
            p = point

        p.transform(self.inversetransform)

        k0 = Vector(p.x / self.radiusX, p.y / self.radiusY, p.z / self.radiusZ).length
        k1 = Vector(p.x / self.radiusX**2, p.y / self.radiusY**2, p.z / self.radiusZ**2).length
        if k1 == 0:
            return -1
        else:
            return k0 * (k0 - 1.0) / k1

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function

        Parameters
        ----------
        x,y,z: `numpy arrays, np.ogrid[]`
            The coordinates of all the points in R:sup:`3` space to query for their distances.
            The shapes are ``x: (nx, 1, 1), y: (1, ny, 1), z: (1, 1, nz)``
        Returns
        -------
        numpy array of floats, shape (nx, ny, nz)
            The distances from the query points to the surface of the object.
        """
        import numpy as np

        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(self.inversetransform, p)
        k0 = np.sqrt(np.square(xt/self.radiusX) + np.square(yt/self.radiusY) + np.square(zt/self.radiusZ))
        k1 = np.sqrt(np.square(xt/self.radiusX**2) + np.square(yt/self.radiusY**2) + np.square(zt/self.radiusZ**2))
        out = np.where(k1 == 0, -1, k0 * (k0 - 1.0) / k1)
        return out


# if __name__ == "__main__":
#     # import numpy as np
#     # import matplotlib.pyplot as plt

#     e = VolEllipsoid(14, 10, 6)
#     print(e)

#     for y in range(-15, 15):
#         s = ''
#         for x in range(-30, 30):
#             d = e.get_distance(Point(x * 0.5, -y, 0))
#             if d < 0:
#                 s += 'x'
#             else:
#                 s += '.'
#         print(s)

#     # x, y, z = np.ogrid[-15:15:61j, -15:15:61j, -15:15:61j]
#     # d = e.get_distance_numpy(x, y, z)
#     # plt.imshow(d[:, :, 30]<0, cmap='RdBu')
#     # plt.axis('equal')
#     # plt.show()
