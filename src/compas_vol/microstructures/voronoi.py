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
        secondc = sortpoints[1][1]
        vc = Vector(*closest)
        vs = Vector(*secondc)
        v1 = Vector(*point) - (vc+vs)/2
        v2 = (vs-vc).unitized()
        return -1*v1.dot(v2) - self.thickness/2

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        return NotImplementedError


if __name__ == "__main__":
    # from compas.geometry import Point
    import numpy as np
    import matplotlib.pyplot as plt
    from compas.geometry import pointcloud_xy

    points = pointcloud_xy(90, (0, 300))
    b = Voronoi(points=points, thickness=2.5)

    # b.get_distance((2,3,4))
    # x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    # m = b.get_distance_numpy(x, y, z)

    # plt.imshow(m[:, :, 25].T, cmap='RdBu')
    # plt.colorbar()
    # plt.axis('equal')
    # plt.show()
    m = np.empty((300, 300))
    for y in range(300):
        s = ''
        for x in range(300):
            d = b.get_distance(Point(x, y, 0))
            m[y,x] = d
            #print(d)
        #     if d < 0:
        #         s += 'x'
        #     else:
        #         s += '.'
        # print(s)
    plt.imshow(m, cmap='RdBu')
    plt.show()
