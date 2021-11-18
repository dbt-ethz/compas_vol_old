from compas.geometry import Frame
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse

class Heart(object):
    """A volumetric heart is defined by its size and a compas.geometry frame

    Parameters
    ----------
    size : float
        Scale factor.
    frame : :class:`compas.geometry.Frame`
        The base frame.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas_vol.primitives import Heart
    >>> frame = Frame((1, 2, 3), (1, 0, 0), (0, 1, 0))))
    >>> heart = Heart(size=4, frame)
    """
    
    def __init__(self, size=3.0, frame=None):
        self.size = size
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
        x, y, z = point
        x /= self.size * 0.43
        y /= self.size * 0.43
        z /= self.size * 0.43
        res = 320 * ((-x**2 * z**3 - 9*y**2 * z**3/80) +
                     (x**2 + 9*y**2/4 + z**2-1)**3)
        return res

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
        xt, yt, zt, _ = np.dot(self.inversetransform, p)
        
        sx, sy, sz = xt / (self.size * 0.43), yt / (self.size * 0.43), zt / (self.size * 0.43)
        return np.full((x.shape[0], y.shape[1], z.shape[2]), 320 * ((-sx**2 * sz**3 - 9*sy**2 * sz**3/80) + (sx**2 + 9*sy**2/4 + sz**2-1)**3))



if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt
    from compas.geometry import Frame

    h = Heart(size=30, frame=Frame((0, 0, 0), (1, 0, 0), (0, 1, 0)))

    x, y, z = np.ogrid[-30:30:60j, -30:30:60j, -30:30:60j]

    d = h.get_distance_numpy(x, y, z)
    m = np.tanh(d[:, 30, :].T)
    plt.imshow(m, cmap='Greys', interpolation='nearest')
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = h.get_distance((x * 0.5, 0, -y))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)