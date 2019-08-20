from compas.geometry.primitives import Plane
from compas.geometry.primitives import Point
from compas.geometry.distance import distance_point_plane_signed


__all__ = ['VolPlane']


class VolPlane(object):
    def __init__(self, plane):
        self.plane = plane

    def get_distance(self, point):
        """
        single point distance function
        """
        return distance_point_plane_signed(point, self.plane)

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        base, normal = self.plane
        x = x-base.x
        y = y-base.y
        z = z-base.z
        d = np.dot(np.array([x, y, z]), normal)
        return d


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    p = VolPlane(Plane((0, 2, 0), (1, 1, 1)))

    x, y, z = np.ogrid[-20:20:40j, -15:15:30j, -10:10:20j]
    print(x.shape, y.shape, z.shape)
    d = p.get_distance_numpy(x, y, z)
    print(d.shape)
    plt.imshow(d[:, :, 10], cmap='RdBu')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = p.get_distance(Point(x * 0.5, 0, -y))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '·'
    #     print(s)
