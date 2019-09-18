from math import sqrt

from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation

__all__ = ['VolBox']


class VolBox(object):
    """A volumetric box is defined by a base box from `compas.geometry` and an optional fillet radius.

    The center of the volumetric box is positioned at the origin of the
    coordinate system defined by the frame. The box is axis-aligned to the frame.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        The base box.
    radius : float
        The filletting radius along the edges, default=0.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Box
    >>> from compas_vol.primitives import VolBox
    >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
    >>> vbx = VolBox(box, 0.3)
    """
    def __init__(self, box, radius=0.0):
        self._box = None
        self.box = box
        self._radius = None
        self.radius = radius

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, box):
        if not isinstance(box, Box):
            raise ValueError
        self._box = box

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def data(self):
        return {'box': self.box.data,
                'radius': self.radius}

    def to_data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.box = Box.from_data(data['box'])
        self.radius = data['radius']

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

        T = Transformation.from_frame(self.box.frame)
        i = T.inverse()
        p.transform(i)

        dx = abs(p.x) - (self.box.xsize / 2.0 - self.radius)
        dy = abs(p.y) - (self.box.ysize / 2.0 - self.radius)
        dz = abs(p.z) - (self.box.zsize / 2.0 - self.radius)
        inside = max(dx, max(dy, dz)) - self.radius
        dx = max(dx, 0)
        dy = max(dy, 0)
        dz = max(dz, 0)
        if inside + self.radius < 0:
            return inside
        else:
            corner = sqrt(dx * dx + dy * dy + dz * dz) - self.radius
            return corner

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function

        Parameters
        ----------
        x,y,z: `numpy arrays, np.ogrid[]`
            The coordinates of all the points in R<sup>3</sup> space to query for their distances.
            The shapes are ``x: (nx, 1, 1), y: (1, ny, 1), z: (1, 1, nz)``
        Returns
        -------
        numpy array of floats, shape (nx, ny, nz)
            The distances from the query points to the surface of the object.
        """
        import numpy as np
        from compas.geometry import matrix_from_frame, inverse

        m = matrix_from_frame(self.box.frame)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)

        # dx = np.abs(xt - self.box.frame.point.x) - (self.box.xsize / 2.0 - self.radius)
        # dy = np.abs(yt - self.box.frame.point.y) - (self.box.ysize / 2.0 - self.radius)
        # dz = np.abs(zt - self.box.frame.point.z) - (self.box.zsize / 2.0 - self.radius)
        dx = np.abs(xt) - (self.box.xsize / 2.0 - self.radius)
        dy = np.abs(yt) - (self.box.ysize / 2.0 - self.radius)
        dz = np.abs(zt) - (self.box.zsize / 2.0 - self.radius)
        inside = np.maximum(dx, np.maximum(dy, dz)) - self.radius
        dx = np.maximum(dx, 0)
        dy = np.maximum(dy, 0)
        dz = np.maximum(dz, 0)

        out = np.where((inside + self.radius) < 0, inside,
                       np.sqrt(dx**2 + dy**2 + dz**2) - self.radius)
        return out


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    box = Box(Frame(Point(3, 2, 0), [1, 0.2, 0.1], [-0.1, 1, 0.1]), 25, 10, 15)
    vb = VolBox(box, 3.0)

    x, y, z = np.ogrid[-15:15:60j, -15:15:60j, -15:15:60j]
    d = vb.get_distance_numpy(x, y, z)
    plt.imshow(d[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    plt.axis('equal')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = vb.get_distance((x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)
