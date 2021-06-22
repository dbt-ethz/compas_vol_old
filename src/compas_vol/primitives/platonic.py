from compas.geometry import Point, Vector, Frame
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
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

    def __init__(self, radius, type=0, frame=None):
        self.radius = radius
        self.type = type
        self.frame = frame or Frame.worldXY()
        self.inversetransform = matrix_inverse(matrix_from_frame(self.frame))
        self.sqrt3 = sqrt(3)
        self.tan30 = tan(pi/6)
    
    def get_distance(self, point):

        if not isinstance(point, Point):
            point = Point(*point)
        point.transform(self.inversetransform)
        x, y, z = point
        
        # Tetrahedron
        if self.type == 0:
            return (max(abs(x + y) - z, abs(x - y) + z) - self.radius) / self.sqrt3
        
        # Octahedron
        elif self.type == 1:
            s = abs(x) + abs(y) + abs(z)
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
            px = abs(x / r)
            py = abs(y / r)
            pz = abs(z / r)

            p = Vector(px, py, pz)
            a = p.dot(v)
            b = p.dot(Vector(v.z, v.x, v.y))
            c = p.dot(Vector(v.y, v.z, v.x))
            d = p.dot([w,w,w]) - v.x
            q = max(max(max(a, b), c) - v.x, d) * r
            return q
        
        else:
            return 0
        
    def get_distance_numpy(self, x, y, z):
        import numpy as np

        p = np.array([x, y, z, 1], dtype=object)
        xt, yt, zt, _ = np.dot(self.inversetransform, p)

        if self.type == 0:
            return (np.maximum(np.abs(xt + yt) - zt, np.abs(xt - yt) + zt) - self.radius) / self.sqrt3
        
        elif self.type == 1:
            return ((np.abs(xt) + np.abs(yt) + np.abs(zt)) - self.radius) * self.tan30
        
        elif self.type == 2:
            v = np.array([(1 + np.sqrt(5)/2, 1, 0)])
            v = np.reshape(np.tile(v / np.linalg.norm(v), xt.size), (*xt.shape, 3))
            p = np.empty((*xt.shape, 3))
            p[:,:,:,0], p[:,:,:,1], p[:,:,:,2] = np.abs(xt/self.radius), np.abs(yt/self.radius), np.abs(zt/self.radius)
            return (np.maximum(np.maximum(np.sum(p * v, axis=3), np.sum(p * np.roll(v, 1, axis=3), axis=3)),
                    np.sum(p * np.roll(v, 2, axis=3), axis=3)) - v[:,:,:,0]) * self.radius
        
        elif self.type == 3:
            r = self.radius * 0.8506507174597755
            v = np.array([(sqrt(5) + 3)/2, 1, 0])
            v = np.reshape(np.tile(v / np.linalg.norm(v), xt.size), (*xt.shape, 3))
            w = np.full((*xt.shape,3), np.sqrt(3)/3)
            p = np.empty((*xt.shape, 3))
            p[:,:,:,0], p[:,:,:,1], p[:,:,:,2] = np.abs(xt/r), np.abs(yt/r), np.abs(zt/r)
            return np.maximum(np.maximum(np.maximum(np.sum(p * v, axis=3), np.sum(p * np.roll(v, 1, axis=3), axis=3)),
                   np.sum(p * np.roll(v, 2, axis=3), axis=3)) - v[:,:,:,0], np.sum(p * w, axis=3) - v[:,:,:,0]) * r
        
        else:
            return np.zeros((*xt.shape,))


if __name__=="__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    p = PlatonicSolid(10.0, 0, frame=Frame((1, 2, 3), (1, 0.3, 0.1), (-0.4, 1, 0.3)))

    x, y, z = np.ogrid[-30:30:60j, -30:30:60j, -30:30:60j]
    start = time.time()
    d = p.get_distance_numpy(x, y, z)
    end = time.time()
    print(end-start)
    m = np.tanh(d[:, :, 30].T)
    plt.imshow(m, cmap='Greys', interpolation='nearest')
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    # p = PlatonicSolid(10.0, 3)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = p.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)