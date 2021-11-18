from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import is_point_in_polygon_xy

class VolExtrusion(object):
    """A volumetric extrusion is defined by a polyline from `compas.geometry` and a height.
    Parameters
    ----------
    polyline: sequence
        A a sequence of (x,y,z) points describing the base polyline.
    height: float
        The height of the extrusion.
    Examples
    --------
    >>> TODO
    """

    def __init__(self, polyline, height=1.0, frame=None):
        self.polyline = polyline
        self.height = height
        self.frame = frame or Frame.worldXY()
        self.inversetransform = matrix_inverse(matrix_from_frame(self.frame))


    def get_distance(self, point):
        """
        single point distance function

        Parameters
        ----------
        point: :class:`compas.geometry.Point`
            The point in R<sup>3</sup> space to query for it's distance.
        Returns
        -------
        float
            The distance from the query point to the surface of the object.
        """

        if not isinstance(point, Point):
            point = Point(*point)

        point.transform(self.inversetransform)

        tp = Point(point[0], point[1], 0)
        cp = closest_point_on_polyline_xy(tp, self.polyline)
        d = tp.distance_to_point(cp)
        if is_point_in_polygon_xy(tp, self.polyline):
            d = -1.*d
        d = max(d, abs(point.z) - self.height / 2.0)
        return d


    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function

        Parameters
        ----------
        x,y,z: `numpy arrays, np.ogrid[]`
            The coordinates of all the points in R:sup:`3` space to query for their distances.
            The shapes are ``x: (nx, 1, 1), y: (1, ny, 1), z: (1, 1, nz)``
        Returns
        -------
        numpy array of floats, shape (nx, ny, nz)
            The distances from the query points to the surface of the object.
        """

        import numpy as np
        l = len(self.polyline)-1
        
        p = np.array([x, y, z, 1], dtype=object)
        xt, yt, zt, _ = np.dot(self.inversetransform, p)
        _xyt = np.empty((*xt.shape, l, 2))
        _xyt[:,:,:,:,0], _xyt[:,:,:,:,1] = np.reshape(np.repeat(xt, l), (*xt.shape, l)), np.reshape(np.repeat(yt, l), (*yt.shape, l))

        v2D = np.empty((l, 3, 2))
        for i in range(l):
            v2D[i,0] = self.polyline[i][0], self.polyline[i][1]
            v2D[i,1] = self.polyline[i+1][0], self.polyline[i+1][1]
            v2D[i,2,0], v2D[i,2,1] = self.polyline[i+1][0] - self.polyline[i][0], self.polyline[i+1][1] - self.polyline[i][1]
        v2D = np.reshape(np.tile(v2D, (xt.size, 1, 1)), (*xt.shape, l, 3, 2))

        w = np.empty((*xt.shape,l,2))
        w[:,:,:,:,0], w[:,:,:,:,1] = _xyt[:,:,:,:,0] - v2D[:,:,:,:,0,0], _xyt[:,:,:,:,1] - v2D[:,:,:,:,0,1]
        b = w - v2D[:,:,:,:,2] * np.clip(np.sum(w * v2D[:,:,:,:,2], axis=4) / np.sum(v2D[:,:,:,:,2]**2, axis=4), 0, 1)[..., np.newaxis]

        cond = np.empty((*xt.shape,l,3), dtype=bool)
        cond[:,:,:,:,0] = _xyt[:,:,:,:,1] >= v2D[:,:,:,:,0,1]  
        cond[:,:,:,:,1] = _xyt[:,:,:,:,1] < v2D[:,:,:,:,1,1]
        cond[:,:,:,:,2] = v2D[:,:,:,:,2,0] * w[:,:,:,:,1] > v2D[:,:,:,:,2,1] * w[:,:,:,:,0]
        s = np.where(np.sum(np.all(cond, axis=4) | np.all(~cond, axis=4), axis=3) %2 != 0, -1, np.ones((xt.shape)))

        return np.maximum(s * np.sqrt(np.min(np.sum(b**2, axis=4), axis=3)), np.abs(zt) - self.height / 2.0)