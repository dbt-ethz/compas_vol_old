from compas import PRECISION


class Shell(object):
    """A shell object converts a solid volumetric object into a constant thickness boundary volume.

    Parameters
    ----------
    obj : :class:`compas_vol`
        The input object.
    thickness : float
        The thickness of the shell.
    side : float
        Side factor.
        For ``s = 1.0``, the shell will be offset to the inside.
        For ``s = 0.5``, the shell will be offset half/half on either side of the original surface.
        For ``s = 0.0``, the shell will be offset to the outside.

    Examples
    --------
    >>> TODO
    """

    def __init__(self, obj, thickness=1.0, side=0.0):
        self.o = obj
        self.thickness = thickness
        self.side = side

    def __repr__(self):
        return 'Shell({0},{1:.{3}f},{2:.{3}f})'.format(str(self.o), self.thickness, self.side, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        do = self.o.get_distance(point)
        return abs(do + (self.side - 0.5) * self.thickness) - self.thickness/2.0

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        do = self.o.get_distance_numpy(x, y, z)
        return np.abs(do + (self.side - 0.5) * self.thickness) - self.thickness/2.0

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":
    from compas_vol.combinations import Union
    from compas_vol.primitives import VolSphere, VolBox
    from compas.geometry import Box, Frame, Point, Sphere

    s = Sphere(Point(5, 6, 0), 9)
    b = Box(Frame.worldXY(), 20, 15, 10)
    vs = VolSphere(s)
    vb = VolBox(b, 2.5)

    u = Union(vs, vb)
    sh = Shell(u, 2.5, 0.5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = sh.get_distance(Point(x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
