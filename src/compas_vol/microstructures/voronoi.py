from math import pi, sin, cos
from compas.geometry import Point

class Voronoi(object):
    """A triply periodic minimal surface (TPMS) is defined by a type and a wavelength.

    Parameters
    ----------
    tpmstype: String
        Type of TPMS. Currently avaliable are Gyroid, SchwartzP, Diamond, Neovius, Lidinoid and FischerKoch.
    wavelength: float
        The wavelength of the trigonometric function.

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
        distances = [point.distance_to_point(p) for p in self.points]
        distances.sort()

        return abs(distances[0] - distances[1]) - self.thickness

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        px = x/self._factor
        py = y/self._factor
        pz = z/self._factor

        d = 0
        return d


if __name__ == "__main__":
    # from compas.geometry import Point
    import numpy as np
    import matplotlib.pyplot as plt
    from compas.geometry import pointcloud

    points = pointcloud(20, (-14, 14))
    b = Voronoi(points=points, thickness=1.0)

    # x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    # m = b.get_distance_numpy(x, y, z)

    # plt.imshow(m[:, :, 25].T, cmap='RdBu')
    # plt.colorbar()
    # plt.axis('equal')
    # plt.show()

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = b.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
