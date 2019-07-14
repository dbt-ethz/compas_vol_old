class Morph(object):
    def __init__(self, a=None, b=None, f=0.5):
        self.a = a
        self.b = b
        self.f = f

    def get_distance(self, point):
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        return (1.0-self.f)*da + self.f*db

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
    u = Morph(vs, vb, 0.5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
