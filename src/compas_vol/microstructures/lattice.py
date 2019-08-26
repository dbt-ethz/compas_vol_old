import math
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation


class Lattice(object):
    def __init__(self, ltype=0, unitcell=1.0, thickness=0.1):
        self.pointlist = self.create_points()
        self.types = self.create_types()
        self.type = ltype
        self.unitcell = unitcell
        self.thickness = thickness
        self.frame = Frame.worldXY()

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def frame(self):
        """Frame: The lattice's frame."""
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = Frame(frame[0], frame[1], frame[2])

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

        types = [bigx, grid, star, cross, octagon, octet, vintile, dual, interlock, isotrop]
        return types

    def get_distance(self, point):
        if not isinstance(point, Point):
            pt = Point(*point)
        else:
            pt = point
        # frame to frame: box to world
        T = Transformation.from_frame(self.frame)
        i = T.inverse()
        pt.transform(i)

        up = [abs((p % self.unitcell) - self.unitcell/2) for p in pt]
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
        """
        vectorized distance function
        """
        import numpy as np
        from compas.geometry import matrix_from_frame, inverse

        m = matrix_from_frame(self.frame)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)

        mg = np.array(np.meshgrid(y, z, x)).T
        mg = abs((mg % self.unitcell) - self.unitcell/2)

        distances = []
        for l in self.types[self.type]:
            A = np.array([self.pointlist[l[0]][i] * self.unitcell for i in range(3)])
            B = np.array([self.pointlist[l[1]][i] * self.unitcell for i in range(3)])
            d = np.linalg.norm(np.cross(B-A, mg-A), axis=-1)/np.linalg.norm(B-A)
            distances.append(d)
        return np.asarray(distances).min(axis=0)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    lat = Lattice(6, 5.0, 0.3)
    lat.frame = Frame((1, 0, 0), (1, 0.2, 0.1), (-0.3, 1, 0.2))

    x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    m = lat.get_distance_numpy(x, y, z)

    # num = 200
    # m = np.empty((num, num))
    # for r in range(num):
    #     for c in range(num):
    #         m[r, c] = lat.get_distance((c, r, 10))
    plt.imshow(m[:, :, 25], cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    plt.axis('equal')
    plt.colorbar()
    plt.show()
