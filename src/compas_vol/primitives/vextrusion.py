from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import is_point_in_polygon_xy
from matplotlib.pyplot import axis

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

        v2D = np.empty((l, 2, 2))
        for i in range(l):
            v2D[i,0] = self.polyline[i][0], self.polyline[i][1]
            v2D[i,1] = self.polyline[i+1][0], self.polyline[i+1][1]
        v2D = np.reshape(np.tile(v2D, (xt.size, 1, 1)), (*xt.shape, l, 2, 2))

        cond0 = _xyt[:,:,:,:,1] > np.minimum(v2D[:,:,:,:,0,1], v2D[:,:,:,:,1,1])
        cond1 = _xyt[:,:,:,:,1] <= np.maximum(v2D[:,:,:,:,0,1], v2D[:,:,:,:,1,1])
        cond2 = _xyt[:,:,:,:,0] <= np.maximum(v2D[:,:,:,:,0,0], v2D[:,:,:,:,1,0])
        cond3 = v2D[:,:,:,:,0,1] != v2D[:,:,:,:,1,1]
        cond4 = _xyt[:,:,:,:,0] <= (_xyt[:,:,:,:,1] - v2D[:,:,:,:,0,1]) * (v2D[:,:,:,:,1,0] - v2D[:,:,:,:,0,0]) / (v2D[:,:,:,:,1,1] - v2D[:,:,:,:,0,1]) + v2D[:,:,:,:,0,0]
        cond5 = v2D[:,:,:,:,0,0] == v2D[:,:,:,:,1,0]

        f = np.where(np.sum(np.where(cond0*cond1*cond2*cond3*cond5 + cond0*cond1*cond2*cond3*cond4, 1, np.zeros((*xt.shape, l), dtype=int)), axis=3) %2 != 0, -1, np.ones((xt.shape)))

        cond6 = (v2D[:,:,:,:,0] == _xyt).all(axis=4) + (v2D[:,:,:,:,1] == _xyt).all(axis=4)
        cond7 = (v2D[:,:,:,:,0] == v2D[:,:,:,:,1]).all(axis=4)
        cond8 = np.arccos(np.sum((_xyt - v2D[:,:,:,:,0]) / np.linalg.norm(_xyt - v2D[:,:,:,:,0]) *
                                 (v2D[:,:,:,:,1] - v2D[:,:,:,:,0]) / np.linalg.norm(v2D[:,:,:,:,1] - v2D[:,:,:,:,0]), axis=4)) > np.pi/2
        cond9 = np.arccos(np.sum((_xyt - v2D[:,:,:,:,1]) / np.linalg.norm(_xyt - v2D[:,:,:,:,1]) *
                                 (v2D[:,:,:,:,0] - v2D[:,:,:,:,1]) / np.linalg.norm(v2D[:,:,:,:,0] - v2D[:,:,:,:,1]), axis=4)) > np.pi/2

        d = np.linalg.norm(np.reshape(np.cross(v2D[:,:,:,:,0] - v2D[:,:,:,:,1], v2D[:,:,:,:,0] - _xyt), (*xt.shape,l,1)), axis=4) / np.linalg.norm(v2D[:,:,:,:,1] - v2D[:,:,:,:,0], axis=4)
        d[cond6] = 0
        d[cond7] = np.linalg.norm(v2D[:,:,:,:,0] - _xyt, axis=4)[cond7]
        d[cond8] = np.linalg.norm(_xyt - v2D[:,:,:,:,0], axis=4)[cond8]
        d[cond9] = np.linalg.norm(_xyt - v2D[:,:,:,:,1], axis=4)[cond9]

        return np.maximum(np.amin(d, axis=3) * f, np.abs(zt) - self.height / 2.0)


if __name__ == "__main__":
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    polyline = []
    a = math.pi*2/10
    r = 10
    for i in range(10):
        tr = r
        if i % 2:
            tr = 5
        x = tr*math.cos(i*a)
        y = tr*math.sin(i*a)
        polyline.append((x, y, 0))
    polyline.append(polyline[0])

    ve = VolExtrusion(polyline, height=20, frame=Frame((1, 2, 3), (1, 0.3, 0.1), (-0.4, 1, 0.3)))

    x, y, z = np.ogrid[-30:30:60j, -15:15:60j, -15:15:60j]

    start = time.time()
    d = ve.get_distance_numpy(x, y, z)
    end = time.time()
    print(end-start)
    m = np.tanh(d[:, :, 50].T)
    plt.imshow(m, cmap='Greys', interpolation='nearest')
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    # m = np.empty((60, 30))
    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = ve.get_distance(Point(x * 0.5, -y, 0))
    #         m[x + 30, y + 15] = d
    #         if d < 0:
    #             s += 'O'
    #         else:
    #             s += '.'
    #     print(s)
    # plt.imshow(m, cmap='RdBu')
    # plt.colorbar()
    # plt.show()