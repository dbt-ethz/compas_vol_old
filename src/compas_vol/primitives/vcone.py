from math import cos
from math import sin

from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import length_vector_xy
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse

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

    @property
    def data(self):
        return self.cone.to_data()

    def to_data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.cone = Cone.from_data(data)
    
    @classmethod
    def from_data(cls, data):
        cone = Cone.from_data(data)
        vcone = cls(cone)
        return vcone

    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)

        frame = Frame.from_plane(self.cone.plane)
        m = matrix_from_frame(frame)
        mi = matrix_inverse(m)
        point.transform(mi)

        dxy = length_vector_xy(point)
        a = 1.1
        c = [sin(a), cos(a)]
        # dot product
        d = sum([i*j for (i, j) in zip(c, [dxy, point.z - self.cone.height])])
        return d

        # IQ : https://www.iquilezles.org/www/articles/distfunctions/distfunctions.htm
        # float sdCone( in vec3 p, in vec2 c )
        # {
        #     // c is the sin/cos of the angle
        #     float q = length(p.xy);
        #     return dot(c,vec2(q,p.z));
        # }

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":

    c = Cone(Circle(Plane((0, 0, -1), (0, 1, 1)), 12.), 20.)
    vc = VolCone(c)

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = vc.get_distance(Point(x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)