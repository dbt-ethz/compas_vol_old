class SmoothIntersection(object):
    def __init__(self, a=None, b=None, r=1.0):
        self.a = a
        self.b = b
        self.r = r

    def get_distance(self, x, y, z):
        da = self.a.get_distance(x, y, z)
        db = self.b.get_distance(x, y, z)
        k = self.r
        h = min(max(0.5 - 0.5 * (db - da) / k, 0), 1)
        return (db * (1 - h) + h * da) + k * h * (1 - h)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere(9)
    b = Box(25, 10, 10)
    u = SmoothIntersection(s, b, 1.5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = u.get_distance(x*0.5, y, 0)
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
