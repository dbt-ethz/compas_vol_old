from compas import PRECISION
from math import log

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

        # return np.minimum.reduce(distances)
        # raise NotImplementedError


if __name__ == "__main__":
    from compas.geometry import Point, Sphere
    from compas_vol.primitives import VolSphere
    import matplotlib.pyplot as plt
    import random
    import numpy as np

    spheres = []
    for i in range(10):
        x = 10-random.random()*20
        y = 10-random.random()*20
        r = 3-random.random()*2
        s = Sphere(Point(x, y, 0), r)
        vs = VolSphere(s)
        spheres.append(vs)
    
    sul = SmoothUnionList(spheres, 2)

    x, y, z = np.ogrid[-15:15:61j, -15:15:61j, -15:15:61j]
    d = sul.get_distance_numpy(x, y, z)
    print (d)
    plt.imshow(d[:, :, 0], cmap='RdBu')
    plt.axis('equal')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = sul.get_distance((x * 0.5, -y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)
