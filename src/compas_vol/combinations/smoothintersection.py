class SmoothIntersection(object):
    def __init__(self, a=None, b=None, r=1.0):
        self.a = a
        self.b = b
        self.r = r

    def get_distance(self, point):
        da = self.a.get_distance(point)
        db = self.b.get_distance(point)
        k = self.r
        h = min(max(0.5 - 0.5 * (db - da) / k, 0), 1)
        return (db * (1 - h) + h * da) + k * h * (1 - h)

    def get_distance_numpy(self, x, y, z):
        import numpy as np

        da = self.a.get_distance_numpy(x, y, z)
        db = self.b.get_distance_numpy(x, y, z)
        h = np.minimum(np.maximum(0.5 - 0.5 * (db - da)/self.r, 0), 1)
        return (db * (1 - h) + h * da) + self.r * h * (1 - h)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere
    import numpy as np
    import matplotlib.pyplot as plt

    s = Sphere(Point(5, 6, 0), 9)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)
    u = SmoothIntersection(vs, vb, 2.5)
    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = u.get_distance(Point(x*0.5, y, 0))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)

    x, y, z = np.ogrid[-15:15:50j, -15:15:50j, -15:15:50j]
    d = u.get_distance_numpy(x, y, z)
    plt.imshow(d[:, :, 25].T, cmap='RdBu')
    plt.colorbar()
    plt.show()
