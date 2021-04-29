class Union(object):
    """The Boolean union between two or more volumetric objects.

    Parameters
    ----------
    a: single volumetric object or list of objects
        First object if the union is of two objects only. If a is a list of objects, b is discarded.
    b: (optional) volumetric object
        Second object if the union is of two objects only.

    Examples
    --------
    >>> s = Sphere(Point(5, 6, 0), 9)
    >>> b = Box(Frame.worldXY(), 20, 15, 10)
    >>> vs = VolSphere(s)
    >>> vb = VolBox(b, 2.5)
    >>> u = Union(vs, vb)
    """
    def __init__(self, a=None, b=None):
        if type(a) == list:
            self.objs = a
        else:
            self.objs = [a, b]

    def add_object(self, o):
        """
        add another object to the union
        """
        self.objs.append(o)

    def __repr__(self):
        obj_strings = [str(o) for o in self.objs]
        return 'Union([{}])'.format(', '.join(obj_strings))

    def get_distance(self, point):
        """
        single point distance function
        """
        ds = [o.get_distance(point) for o in self.objs]
        return min(ds)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        distances = ([o.get_distance_numpy(x, y, z) for o in self.objs])
        return np.minimum.reduce(distances)
        # alternative:
        # d = np.asarray([o.get_distance_numpy(x, y, z) for o in self.objs]).min(axis=0)
