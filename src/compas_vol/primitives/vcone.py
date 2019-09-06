from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Plane

__all__ = ['VolCone']


class VolCone(object):
    """A volumetric cone is defined by a base cone from `compas.geometry`.

    Parameters
    ----------
    cone: :class:`compas.geometry.Cone`
        The base cone.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cone = Cone(circle, 7)
    >>> vcone = VolCone(cone)
    """
    def __init__(self, cone):
        self.cone = cone

    def get_distance(self, point):
        raise NotImplementedError

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":

    c = Cone(Circle(Plane((0, 0, 0), (0, 0, 1)), 3.), 4.)
    vc = VolCone(c)
