from compas import PRECISION


class Blend(object):
    def __init__(self, a=None, b=None, c=None, r=1.0):
        self.a = a
        self.b = b
        self.c = c
        self.r = r

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
            return (1 - f) * da + f * db
    
    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        raise NotImplementedError