from compas.geometry import Point

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
    
    def get_distance(self, point):
        return 0
    
    def get_distance_numpy(self, x, y, z):
        import numpy as np
        return 0