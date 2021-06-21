from compas.geometry import Point, Vector
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

    References
    ----------
    adapted from SDF library by Michael Fogleman [1]_

    ..[1] https://github.com/fogleman/sdf/blob/main/sdf/d3.py#L283
    """

    def __init__(self, radius, type=0):
        self.radius = radius;
        self.type = type;
        self.sqrt3 = sqrt(3)
        self.tan30 = tan(pi/6)
    
    def get_distance(self, point):
        x, y, z = point
        
        # Tetrahedron
        if self.type == 0:
            return (max(abs(x + y) - z, abs(x - y) + z) - self.radius) / self.sqrt3
        
        # Octahedron
        elif self.type == 1:
            s = abs(x) + abs(y) + abs(z)
            # s = sum([abs(v) for v in point])
            return (s - self.radius) * self.tan30
        
        # Dodecahedron
        elif self.type == 2:
            v = Vector((1+sqrt(5))/2, 1, 0)
            v.unitize()
            px = abs(x / self.radius)
            py = abs(y / self.radius)
            pz = abs(z / self.radius)
            p = Vector(px, py, pz)
            a = p.dot(v)
            b = p.dot(Vector(v.z, v.x, v.y))
            c = p.dot(Vector(v.y, v.z, v.x))
            q = (max(max(a, b), c) - v.x) * self.radius
            return q
        
        # Icosahedron
        elif self.type == 3:
            r = self.radius * 0.8506507174597755
            v = Vector((sqrt(5) + 3)/2, 1, 0)
            v.unitize()
            w = sqrt(3)/3
            px = abs(x / self.radius)
            py = abs(y / self.radius)
            pz = abs(z / self.radius)
            p = Vector(px, py, pz)
            a = p.dot(v)
            b = p.dot(Vector(v.z, v.x, v.y))
            c = p.dot(Vector(v.y, v.z, v.x))
            d = p.dot([w,w,w]) - v.x
            q = max(max(max(a, b), c) - v.x, d) * self.radius
            return q
        
        else:
            return 0
        
    def get_distance_numpy(self, x, y, z):
        import numpy as np
        return 0

if __name__=="__main__":
    p = PlatonicSolid(10.0,0)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = p.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)