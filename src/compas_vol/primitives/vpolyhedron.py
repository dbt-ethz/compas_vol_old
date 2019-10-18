from compas.geometry import Plane
from compas_vol.primitives import VolPlane

__all__ = ['VolPolyhedron']


class VolPolyhedron(object):
    """
    Class for convex polyhedra delimited by a list of planes.

    Parameters
    ----------
    planes : list of :class:`compas_vol.primitives.VolPlane`
        The list of delimiting planes.
    """

    def __init__(self, planes):
        self.planes = planes or []
        # print(self.planes[-1].plane)

    def get_distance(self, point):
        """
        single point distance function
        intersection of all the delimiting planes
        """
        distances = [p.get_distance(point) for p in self.planes]
        return max(distances)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        distances = ([p.get_distance_numpy(x, y, z) for p in self.planes])
        return np.maximum.reduce((distances))


if __name__ == "__main__":
    import math

    a = math.pi*2 / 7
    planes = []
    for i in range(7):
        x = math.cos(i*a)
        y = math.sin(i*a)
        p = Plane((9*x, 9*y, 0), (x, y, 0))
        vp = VolPlane(p)
        planes.append(vp)
    planes.append(VolPlane(Plane((0, 0, 4), (0, 0, 1))))
    planes.append(VolPlane(Plane((0, 0, -4), (0, 0, -1))))
    vh = VolPolyhedron(planes)

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = vh.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
