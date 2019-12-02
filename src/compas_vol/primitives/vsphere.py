from compas.geometry import Point
from compas.geometry import Sphere
from compas import PRECISION

__all__ = ['VolSphere']


class VolSphere(object):
    """A volumetric sphere is defined by a base sphere from `compas.geometry`.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        The base sphere.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Sphere
    >>> from compas_vol.primitives import VolSphere
    >>> cs = Sphere(Point(1, 1, 1), 5)
    >>> vs = VolSphere(cs)
    """
    def __init__(self, sphere):
        self._sphere = None
        self.sphere = sphere

    @property
    def sphere(self):
        return self._sphere

    @sphere.setter
    def sphere(self, sphere):
        if not isinstance(sphere, Sphere):
            raise ValueError
        self._sphere = sphere

    @property
    def data(self):
        return {'type': self.__class__.__name__,
                'geom': self.sphere.data}

    def to_data(self):
        return self.data

    def from_data(cls, data):
        sphere = Sphere.from_data(data['geom'])
        vsphere = cls(sphere)
        return vsphere

    def __repr__(self):
        return 'VolSphere({})'.format(str(self.sphere))

    def get_distance(self, point):
        if not isinstance(point, Point):
            point = Point(*point)
        d = point.distance_to_point(self.sphere.center)
        return d - self.sphere.radius

    def get_distance_numpy(self, x, y, z):
        import numpy as np
        d = np.sqrt((x - self.sphere.center.x)**2 +
                    (y - self.sphere.center.y)**2 +
                    (z - self.sphere.center.z)**2) - self.sphere.radius
        return d


if __name__ == "__main__":
    o = VolSphere(Sphere(Point(4, 2, 0), 8.5))

    print(str(o))

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = o.get_distance(Point(x * 0.5, 0, -y))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        # print(s)
