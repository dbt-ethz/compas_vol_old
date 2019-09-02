from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import length_vector_xy
from compas.geometry import inverse
from compas.geometry import matrix_from_frame

__all__ = ['VolCylinder']


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

    # ==========================================================================
    # distance functions
    # ==========================================================================

    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)

        frame = Frame.from_plane(self.cylinder.plane)
        m = matrix_from_frame(frame)
        mi = inverse(m)
        point.transform(mi)

        dxy = length_vector_xy(point) #distance_point_point_xy(self.cylinder.center, point)
        d = dxy - self.cylinder.radius
        d = max(d, abs(point.z) - self.cylinder.height / 2.0)
        return d

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np
        from compas.geometry import matrix_from_frame, inverse

        frame = Frame.from_plane(self.cylinder.plane)
        m = matrix_from_frame(frame)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)

        d = np.sqrt(xt**2 + yt**2) - self.cylinder.radius
        out = np.maximum(d, np.abs(zt) - self.cylinder.height / 2.0)
        return out


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import numpy as np
    from compas.geometry import Circle, Plane
    import matplotlib.pyplot as plt

    o = VolCylinder(Cylinder(Circle(Plane([1, 2, 3], [0.3, 0.4, 1.]), 5.0), 7.0))

    x, y, z = np.ogrid[-15:15:60j, -15:15:60j, -15:15:60j]
    d = o.get_distance_numpy(x, y, z)
    plt.imshow(abs(d[:, :, 30].T), cmap='RdBu') # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    plt.axis('equal')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = o.get_distance(Point(x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)
