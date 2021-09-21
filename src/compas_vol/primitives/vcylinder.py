from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import length_vector_xy
from compas.geometry import matrix_inverse
from compas.geometry import matrix_from_frame


class VolCylinder(object):
    """A volumetric cylinder is defined by a base cylinder from `compas.geometry`.

    Parameters
    ----------
    cylinder: :class:`compas.geometry.Cylinder`
        The base cylinder.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cylinder = Cylinder(circle, 7)
    >>> vcylinder = VolCylinder(cylinder)
    """

    def __init__(self, cylinder):
        self.cylinder = cylinder
        frame = Frame.from_plane(self.cylinder.plane)
        transform = matrix_from_frame(frame)
        self.inversetransform = matrix_inverse(transform)

    @property
    def data(self):
        return self.cylinder.data

    def to_data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.cylinder = Cylinder.from_data(data)

    @classmethod
    def from_data(cls, data):
        cylinder = Cylinder.from_data(data)
        vcylinder = cls(cylinder)
        return vcylinder

    def __repr__(self):
        return 'VolCylinder({})'.format(str(self.cylinder))

    # ==========================================================================
    # distance functions
    # ==========================================================================

    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)

        point.transform(self.inversetransform)

        dxy = length_vector_xy(point)  # distance_point_point_xy(self.cylinder.center, point)
        d = dxy - self.cylinder.radius
        d = max(d, abs(point.z) - self.cylinder.height / 2.0)
        return d

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        p = np.array([x, y, z, 1], dtype=object)
        xt, yt, zt, _ = np.dot(self.inversetransform, p)

        d = np.sqrt(xt**2 + yt**2) - self.cylinder.radius
        out = np.maximum(d, np.abs(zt) - self.cylinder.height / 2.0)
        return out
