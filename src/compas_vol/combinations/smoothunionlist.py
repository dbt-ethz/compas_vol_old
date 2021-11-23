from compas import PRECISION
from math import log
from compas.geometry import Point

class SmoothUnionList(object):
    """The smooth union of a list of volumetric objects.

    Parameters
    ----------
    a: list of volumetric objects
    k: float
        Intensity factor. The smaller the number, the stronger the smoothing.

    Examples
    --------
    >>> 
    """
    def __init__(self, a=None, k=1.0):
        self.distance_objects = a
        self.k = k

    def __repr__(self):
        return ''
    
    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            p = Point(*point)
        else:
            p = point
        res = 0
        d = 0
        for do in self.distance_objects:
            d = do.get_distance(point)
            res += pow(2, -self.k * d)
        return -log(res, 2) / self.k

    def get_distance_numpy(self, x, y, z):
        import numpy as np

        distances = np.array([o.get_distance_numpy(x, y, z) for o in self.distance_objects]).T
        res = np.sum(np.power(2, np.full((distances.shape), -self.k) * distances), axis=3)
        return -np.log2(res)/self.k
