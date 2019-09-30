class Overlay(object):
    def __init__(self, a=None, b=None, f=0.1):
        self.a = a
        self.b = b
        self.f = f

    def get_distance(self, point):
        """
        single point distance function
        """
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        return da + self.f * db

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        return da + self.f * db


if __name__ == "__main__":
    from compas_vol.primitives import Box, Plane
    b = Box(22, 20, 15, 5)
    p = Plane(1, 0, 0)
    f = Overlay(b, p, 0.2)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = f.get_distance(x*0.5, y, 0)
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
