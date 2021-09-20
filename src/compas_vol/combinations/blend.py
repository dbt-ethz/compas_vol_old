from compas import PRECISION


class Blend(object):
    def __init__(self, a=None, b=None, c=None, r=1.0, t=0):
        self.a = a
        self.b = b
        self.c = c
        self.r = r
        self.t = t

    def __repr__(self):
        return "Blend({0},{1},{2},{3:.{3}f})".format(str(self.a), str(self.b), str(self.c), self.r, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        dc = self.c.get_distance(point)
        if dc < -self.r/2:
            return da
        elif dc > self.r/2:
            return db
        else:
            f = dc / self.r + 0.5
            if self.t==0:
                return (1 - f) * da + f * db
            elif self.t==1:
                qf = 2 * f**2 if f < 0.5 else 1 - pow(-2 * f + 2, 2) / 2
                return (1 - qf) * da + qf * db
    
    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        d = np.empty((x.shape[0], y.shape[1], z.shape[2]))
        f = np.empty((x.shape[0], y.shape[1], z.shape[2]))

        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        dc = self.c.get_distance_numpy(x, y, z)
        cond1 = dc < -self.r/2
        cond2 = dc > self.r/2
        cond3 = ~cond1 * ~cond2

        d[cond1] = da[cond1]
        d[cond2] = db[cond2]

        if self.t == 0:
            f[cond3] = dc[cond3] / self.r + 0.5
            d[cond3] = (1 - f[cond3]) * da[cond3] + f[cond3] * db[cond3]

        return d

        # # if self.t == 0:

  
        # raise NotImplementedError

if __name__ == "__main__":
    import numpy as np

    from compas.geometry import Point, Plane, Circle, Sphere, Cone
    from compas_vol.primitives import VolSphere, VolCone
    from compas_vol.microstructures import Lattice

    x, y, z = np.ogrid[-30:30:60j,-30:30:60j,-30:30:60j]

    c = VolCone(Cone(Circle(Plane((0, 0, 0), (0, 1, 0)), 20.), 10.))
    s = VolSphere(Sphere(Point(0,0,0), 6.5))
    l = Lattice(1, 10, 0.5)

    b = Blend(c, s, l)

    d = b.get_distance_numpy(x, y, z)

    # spheres = []
    # for i in range(10):
    #     x = 10-random.random()*20
    #     y = 10-random.random()*20
    #     r = 3-random.random()*2
    #     s = Sphere(Point(x, y, 0), r)
    #     vs = VolSphere(s)
    #     spheres.append(vs)
    
    # sul = SmoothUnionList(spheres, 0.8)


