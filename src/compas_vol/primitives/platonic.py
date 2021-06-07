from compas.geometry import Point
from math import sqrt, tan, pi

class PlatonicSolid(object):
    """A platonic solid, defined by radius and type.

    Parameters
    ----------
    radius : float
        The radius of the solid.
    type : int
        The type of solid (tetrahedron, octahedron, dodecahedron, isosahedron)

    Examples
    --------
    >>> ...
    """

    def __init__(self, radius, type=0):
        self.radius = radius;
        self.type = type;
        self.sqrt3 = sqrt(3)
        self.tan30 = tan(pi/6)
    
    def get_distance(self, point):
        x, y, z = point
        if self.type == 0:
            return (max(abs(x + y) - z, abs(x - y) + z) - self.radius) / self.sqrt3
        elif self.type == 1:
            s = abs(x) + abs(y) + abs(z)
            # s = sum([abs(v) for v in point])
            return (s - self.radius) * self.tan30
        elif self.type == 2:
            return 0
        else:
            return 0
        
    def get_distance_numpy(self, x, y, z):
        import numpy as np
        return 0