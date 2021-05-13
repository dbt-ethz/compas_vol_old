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
        raise NotImplementedError