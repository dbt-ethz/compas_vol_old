class Subtraction(object):
    """The Boolean subtraction of one volumetric object from another volumetric object.

    Parameters
    ----------
    a: volumetric object
        Object to subtract from.
    b: volumetric object
        Object to subtract.

    Examples
    --------
    >>> s = Sphere(Point(5, 6, 0), 9)
    >>> b = Box(Frame.worldXY(), 20, 15, 10)
    >>> vs = VolSphere(s)
    >>> vb = VolBox(b, 2.5)
    >>> s = Subtraction(vs, vb)
    """
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __repr__(self):
        return 'Subtraction({},{})'.format(str(self.a), str(self.b))

    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        return max(da, -db)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        return np.maximum(da, -db)
