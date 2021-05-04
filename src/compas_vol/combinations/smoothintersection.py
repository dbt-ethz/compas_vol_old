from compas import PRECISION


class SmoothIntersection(object):
    """The smooth union between two volumetric objects.

    Parameters
    ----------
    a: volumetric object
        First object to intersect.
    b: volumetric object
        Second object to intersect.
    r: float
        Intensity factor, the higher the number, the smoother the result. Default value `1.0`

    Examples
    --------
    >>> s = Sphere(Point(5, 6, 0), 9)
    >>> b = Box(Frame.worldXY(), 20, 15, 10)
    >>> vs = VolSphere(s)
    >>> vb = VolBox(b, 2.5)
    >>> u = SmoothIntersection(vs, vb, 1.5)
    """
    def __init__(self, a=None, b=None, r=1.0):
        self.a = a
        self.b = b
        self.r = r

    def __repr__(self):
        return 'SmoothIntersection({0},{1},{2:.{3}f})'.format(str(self.a), str(self.b), self.r, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        k = self.r
        h = min(max(0.5 - 0.5 * (db - da) / k, 0), 1)
        return (db * (1 - h) + h * da) + k * h * (1 - h)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        h = np.minimum(np.maximum(0.5 - 0.5 * (db - da)/self.r, 0), 1)
        return (db * (1 - h) + h * da) + self.r * h * (1 - h)
