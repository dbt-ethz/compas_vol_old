class Heart(object):
    def __init__(self, size):
        self.size = size

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
        
        sx, sy, sz = x / (self.size * 0.43), y / (self.size * 0.43), z / (self.size * 0.43)
        return np.full((x.shape[0], y.shape[1], z.shape[2]), 320 * ((-sx**2 * sz**3 - 9*sy**2 * sz**3/80) + (sx**2 + 9*sy**2/4 + sz**2-1)**3))



if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt

    h = Heart(30)

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