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
        # return -1 * v1.dot(v2) - self.thickness/2

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        #alldistances = [((x - p[0])**2 + (y - p[1])**2 + (z - p[2])**2) for p in self.points]

        raise NotImplementedError
