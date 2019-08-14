import math


class Lattice(object):
    def __init__(self, ltype=0, unitcell=1.0, thickness=0.1):
        self.pointlist = self.create_points()
        self.types     = self.create_types()
        self.type      = ltype
        self.unitcell  = unitcell
        self.thickness = thickness

    def create_points(self):
        v1 = 0.0
        v2 = 0.5
        v3 = 0.25
        
        points = []
        
        points.append((v1, v1, v1))
        points.append((v2, v1, v1))
        points.append((v2, v2, v1))
        points.append((v1, v2, v1))

        points.append((v1, v1, v2))
        points.append((v2, v1, v2))
        points.append((v2, v2, v2))
        points.append((v1, v2, v2))

        points.append((v3, v1, v1))
        points.append((v2, v3, v1))
        points.append((v3, v2, v1))
        points.append((v1, v3, v1))

        points.append((v1, v1, v3))
        points.append((v2, v1, v3))
        points.append((v2, v2, v3))
        points.append((v1, v2, v3))

        points.append((v3, v1, v2))
        points.append((v2, v3, v2))
        points.append((v3, v2, v2))
        points.append((v1, v3, v2))

        return points

    def create_types(self):
        bigx = [(0, 6)]
        grid = [(6, 2), (6, 5), (6, 7)]
        star = grid + bigx
        cross = [(1, 6), (3, 6), (4, 6)]
        octagon = [(1, 3), (3, 4), (4, 1)]
        octet = cross + octagon
        vintile = [(8, 13), (13, 17), (17, 18), (18, 15), (15, 11), (11, 8)]
        dual = [(0, 1), (0, 3), (0, 4)]
        interlock = grid+dual
        isotrop = [(0, 1), (2, 1), (5, 1), (7, 1), (3, 7), (6, 7), (4, 7)]

        return [bigx, grid, star, cross, octagon, octet, vintile, dual, interlock, isotrop]

    def get_distance(self, point):
        x, y, z = point

        up = [abs((p % self.unitcell) - self.unitcell/2) for p in point]
        dmin = 9999999.
        for l in self.types[self.type]:
            sp = [self.pointlist[l[0]][i] * self.unitcell for i in range(3)]
            ep = [self.pointlist[l[1]][i] * self.unitcell for i in range(3)]
            v = [ep[i]-sp[i] for i in range(3)]
            d = [up[i]-sp[i] for i in range(3)]
            # dot products
            c2 = sum([i*j for (i, j) in zip(v, v)])
            c1 = sum([i*j for (i, j) in zip(d, v)])

            b = c1/c2
            p = [sp[i] + b * v[i] for i in range(3)]
            dmin = min(dmin, sum([(up[i]-p[i])**2 for i in range(3)]))
        return math.sqrt(dmin) - self.thickness/2.0

    def get_distance_numpy(self, x, y, z):
        pass


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    lat = Lattice(6, 20.0, 7)
    m = np.empty((100, 100))
    for r in range(100):
        for c in range(100):
            m[r, c] = lat.get_distance((c, r, 10))
    plt.imshow(m, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    plt.axis('equal')
    plt.colorbar()
    plt.show()
