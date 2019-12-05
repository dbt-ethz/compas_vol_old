from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse

__all__ = ['VolTransformation']


class VolTransformation(object):
    def __init__(self, distobj=None, frame=Frame.worldXY()):
        self.distobj = distobj
        self.frame = frame
        transform = matrix_from_frame(self.frame)
        self.inversetransform = matrix_inverse(transform)

    def __repr__(self):
        return 'VolTransformation({},{})'.format(str(self.distobj), str(self.frame))

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
            p = Point(*point)
        else:
            p = point
        p.transform(self.inversetransform)
        return self.distobj.get_distance(p)

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
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(self.inversetransform, p)
        return self.distobj.get_distance_numpy(xt, yt, zt)


if __name__ == "__main__":
    from compas_vol.microstructures import TPMS

    t = TPMS(wavelength=4)
    tr = VolTransformation(t, Frame((1, 2, 3), (1, 0.3, 0.2), (-0.1, 1, -0.1)))

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = tr.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
