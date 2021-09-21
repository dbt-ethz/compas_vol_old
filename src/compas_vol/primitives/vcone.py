from math import cos
from math import sin

from compas.geometry import Cone
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import length_vector_xy
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse


class VolCone(object):
    """A volumetric cone is defined by a base cone from `compas.geometry`.

    Parameters
    ----------
    cone: :class:`compas.geometry.Cone`
        The base cone.

    Examples
    --------
    >>> from compas.geometry import Plane, Circle, Cone
    >>> from compas_vol.primitives import VolCone
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cone = Cone(circle, 7)
    >>> vcone = VolCone(cone)
    """

    def __init__(self, cone):
        self.cone = cone
        self.frame = Frame.from_plane(self.cone.plane)
        self.matrix = matrix_from_frame(self.frame)
        self.inversedmatrix = matrix_inverse(self.matrix)

    @property
    def data(self):
        return self.cone.to_data()

    def to_data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.cone = Cone.from_data(data)

    @classmethod
    def from_data(cls, data):
        cone = Cone.from_data(data)
        vcone = cls(cone)
        return vcone

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
            point = Point(*point)

        point.transform(self.inversedmatrix)

        dxy = length_vector_xy(point)
        a = 1.1
        c = [sin(a), cos(a)]
        d =  sum([i*j for (i, j) in zip(c, [dxy, point.z - self.cone.height])])
        return d


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
        
        p = np.array([x, y, z, 1], dtype=object)
        xt, yt, zt, _ = np.dot(self.inversedmatrix, p)

        f = (zt + self.cone.height / 2) / self.cone.height
        temprad = self.cone.radius + f * -self.cone.radius
        dxy = np.sqrt(xt**2 + yt**2) - temprad
        d = np.maximum(dxy, np.abs(zt) - self.cone.height / 2)

        return d
        # c = np.full((*xt.shape, 2), [np.sin(1.1), np.cos(1.1)])
        # h = (zt - self.cone.height) * np.sin(1.1)
        # print(h)

        # double f = (point.Z + this.height / 2) / this.height;
        # double temprad = this.radiusa + f * (this.radiusb - this.radiusa);
        # double dxy = Math.Sqrt(point.X * point.X + point.Y * point.Y) - temprad;
        # double dist = Math.Max(dxy, Math.Abs(point.Z) - height / 2.0);




        # dxy = np.empty((*xt.shape,2))
        # dxy[:,:,:,0], dxy[:,:,:,1] = np.sqrt(xt**2 + yt**2), zt - self.cone.height

        # return np.sum(np.full((*xt.shape,2), [np.sin(1.1), np.cos(1.1)]) * dxy, axis=3)


if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt

    c = Cone(Circle(Plane((0, 10, 0), (0, 1, 0)), 10.), 5.)
    vc = VolCone(c)

    x, y, z = np.ogrid[-30:30:60j, -15:15:60j, -15:15:60j]

    d = vc.get_distance_numpy(x, y, z)




    m = np.tanh(d[:, :, 30].T)
    plt.imshow(m, cmap='Greys', interpolation='nearest')
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    # for y in range(-30, 30):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = vc.get_distance(Point(x, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)