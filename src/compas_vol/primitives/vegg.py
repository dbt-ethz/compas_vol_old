from compas.geometry import Frame, Point
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse

class VolEgg (object):
    """A volumetric egg...

    Parameters
    ----------
    ...

    Examples
    --------
    >>>
    """

    def __init__(self, radiusA=3, radiusB=4, k=0.1, frame=Frame.worldXY()):
        self.ra = radiusA
        self.rb = radiusB
        self.k = k
        self.frame = frame
        self.matrix = matrix_from_frame(self.frame)
        self.inversedmatrix = matrix_inverse(self.matrix)

    
    # ==========================================================================
    # distance functions
    # ==========================================================================
    
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

        point.transform(self.inversedmatrix)

        d = ((point.z * point.z) / (self.rb * self.rb)) + ((point.y *point.y) / (self.ra * self.ra)) + ((point.x * point.x) / (self.ra * self.ra)) * (1 + self.k * point.z) - 1
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

        p = np.array([x, y, z, 1], dtype=object)
        xt, yt, zt, _ = np.dot(self.inversedmatrix, p)

        d = ((zt * zt) / (self.rb * self.rb)) + ((yt * yt) / (self.ra * self.ra)) + ((xt * xt) / (self.ra * self.ra)) * (1 + self.k * zt) - 1
        return d