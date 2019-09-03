class Intersection(object):
    """The Boolean intersection between two or more volumetric objects.

    Parameters
    ----------
    a: single volumetric object or list of objects
        First object if the intersection is of two objects only. If a is a list of objects, b is discarded.
    b: (optional) volumetric object
        Second object if the intersection is of two objects only.

    Examples
    --------
    >>> s = Sphere(Point(5, 6, 0), 9)
    >>> b = Box(Frame.worldXY(), 20, 15, 10)
    >>> vs = VolSphere(s)
    >>> vb = VolBox(b, 2.5)
    >>> i = Intersection(vs, vb)
    """
    def __init__(self, a=None, b=None):
        if type(a) == list:
            self.objs = a
        else:
            self.objs = [a, b]

    def get_distance(self, point):
        """
        single point distance function
        """
        ds = [o.get_distance(point) for o in self.objs]
        return max(ds)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        # da = self.objs[0].get_distance_numpy(x, y, z)
        # db = self.objs[1].get_distance_numpy(x, y, z)
        # return np.maximum(da, db)
        distances = ([o.get_distance_numpy(x, y, z) for o in self.objs])
        return np.maximum.reduce((distances))

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere

    s = Sphere(Point(5, 6, 0), 9)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)
    u = Intersection(vs, vb)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(Point(x * 0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
