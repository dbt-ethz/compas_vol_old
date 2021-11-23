class Multiplication(object):
    """
    The multiplication of two or more scalar fields defined by volumetric objects.

    Parameters
    ----------
    a: volumetric object
        First object
    b: volumetric object
        Second object
    """

    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b
    
    def __repr__(self) -> str:
        obj_strings = [str(o) for o in self.objs]
        return 'Multiplication([{}])'.format(', '.join(obj_strings))
    
    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        return da*db

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        da = self.a.get_distance_numpy(x,y,z)
        db = self.b.get_distance_numpy(x,y,z)
        return np.multiply(da, db)