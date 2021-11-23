class Addition(object):
    """
    The addition of two or more scalar fields defined by volumetric objects.

    Parameters
    ----------
    a: single volumetric object or list of objects
        First object
    b: (optional) volumetric object
        Second object if the addition is of two objects only.
    """

    def __init__(self, a=None, b=None):
        if type(a) == list:
            self.objs = a
        else:
            self.objs = [a, b]
    
    def __repr__(self) -> str:
        obj_strings = [str(o) for o in self.objs]
        return 'Addition([{}])'.format(', '.join(obj_strings))
    
    def get_distance(self, point):
        """
        single point distance function
        """
        ds = [o.get_distance(point) for o in self.objs]
        return sum(ds)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        distances = ([o.get_distance_numpy(x, y, z) for o in self.objs])
        return np.sum(distances, axis=0)