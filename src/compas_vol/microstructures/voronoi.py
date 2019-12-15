from compas.geometry import Point
from compas.geometry import Vector


class Voronoi(object):
    """A Voronoi....

    Parameters
    ----------
    points : String
        Type of TPMS. Currently avaliable are Gyroid, SchwartzP, Diamond, Neovius, Lidinoid and FischerKoch.
    thickness : float
        The wavelength of the trigonometric function.
    walls : bool

    Examples
    --------
    >>> a = TPMS(tpmstype='Gyroid', wavelength=5.0)
    """
    def __init__(self, points=None, thickness=1.0, walls=True):
        self.thickness = thickness
        self.points = points
        self.walls = walls

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def thickness(self):
        """float: The thickness of the cell separation walls."""
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        self._thickness = float(thickness)

    # ==========================================================================
    # distance function
    # ==========================================================================

    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)

        distances = [(point.distance_to_point(p), p) for p in self.points]
        sortpoints = sorted(distances, key=lambda x: x[0])
        closest = sortpoints[0][1]

        vc = Vector(*closest)
        d1 = vc.dot(vc)

        secondc = sortpoints[1][1]
        vs = Vector(*secondc)
        v1 = Vector(*point) - (vc+vs)/2
        v2 = (vs-vc).unitized()

        d2 = v1.dot(v2)

        return abs(min(d1, d2)) - self.thickness/2
        #return -1 * v1.dot(v2) - self.thickness/2

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        alldistances = [((x - p[0])**2 + (y - p[1])**2 + (z - p[2])**2) for p in self.points]
        
        print(len(alldistances), type(alldistances[0]))


if __name__ == "__main__":
    # from compas.geometry import Point
    import numpy as np
    import matplotlib.pyplot as plt
    from compas.geometry import pointcloud_xy

    dim = 300
    points = pointcloud_xy(66, (0, dim))
    b = Voronoi(points=points, thickness=2.5)

    # b.get_distance((2,3,4))
    #x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    #m = b.get_distance_numpy(x, y, z)

    # plt.imshow(m[:, :, 25].T, cmap='RdBu')
    # plt.colorbar()
    # plt.axis('equal')
    # plt.show()

    m = np.empty((dim, dim))
    for y in range(dim):
        s = ''
        for x in range(dim):
            d = b.get_distance(Point(x, y, 0))
            m[y, x] = min(d, 25)
            #print(d)
        #     if d < 0:
        #         s += 'x'
        #     else:
        #         s += '.'
        # print(s)
    # print(m.min(), m.max())
    plt.imshow(m, cmap='gnuplot2')
    plt.show()
