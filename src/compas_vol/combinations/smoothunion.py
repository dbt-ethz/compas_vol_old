class SmoothUnion(object):
    def __init__(self, a=None, b=None, r=1.0):
        self.a = a
        self.b = b
        self.r = r

    def get_distance_(self, x, y, z):
        da = self.a.get_distance(x, y, z)
        db = self.b.get_distance(x, y, z)
        e = max(self.r - abs(da - db), 0)
        return min(da, db) - e**2 * 0.25 / self.r

    def get_distance(self, point):
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        k = self.r
        h = min(max(0.5 + 0.5 * (db - da) / k, 0), 1)
        return (db * (1 - h) + h * da) - k * h * (1 - h)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere

    s = Sphere(Point(5, 6, 0), 9)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)
    u = SmoothUnion(vs, vb, 2.5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
