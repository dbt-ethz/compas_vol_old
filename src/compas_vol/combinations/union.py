class Union(object):
    def __init__(self, a=None, b=None):
        if type(a) == list:
            self.objs = a
        else:
            self.objs = [a, b]

    def get_distance(self, point):
        ds = [o.get_distance(point) for o in self.objs]
        return min(ds)

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
    u = Union(vs, vb)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
