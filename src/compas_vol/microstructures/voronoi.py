from compas.geometry import Point
from compas.geometry import Vector
from matplotlib.pyplot import axis
from numpy.core.fromnumeric import argsort


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
        v2 = vs-vc
        v2.unitize()
        d2 = v1.dot(v2)

        return abs(min(d1, d2)) - self.thickness/2


    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        p = np.reshape(np.repeat(np.stack((np.meshgrid(y, x, z)), axis=3), len(self.points), axis=2), 
            (x.shape[0], y.shape[1], z.shape[2], len(self.points), 3))

        coords = np.reshape(np.tile(np.array([[p.x, p.y, p.z] for p in self.points]), (x.size * y.size * z.size, 1)),
                 (x.shape[0], y.shape[1], z.shape[2], len(self.points), 3))
        coords = np.concatenate((coords, np.linalg.norm(p - coords, axis=4, keepdims=True)), axis=4)
        closestPts = np.take_along_axis(coords, coords[:,:,:,:,-1].argsort()[..., None], axis=3)[:,:,:,:2,:3]

        d1 = np.sum(closestPts[:,:,:,0]**2, axis=3)
        v1 = np.stack((np.meshgrid(y, x, z)), axis=3) - (closestPts[:,:,:,0] + closestPts[:,:,:,1]) / 2
        v2 = (closestPts[:,:,:,1] - closestPts[:,:,:,0]) / np.linalg.norm(closestPts[:,:,:,1] - closestPts[:,:,:,0], axis=3, keepdims=True)
        d2 = np.sum(v1 * v2, axis=3)

        return np.abs(np.minimum(d1, d2)) - self.thickness / 2