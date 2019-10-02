from compas.geometry import Frame
from compas.geometry import Plane
from compas_vol.primitives import VolPlane
from compas.geometry import distance_point_plane_signed
from compas.geometry import rotate_points
from compas.geometry import matrix_from_axis_and_angle
from compas_vol.primitives import VolPlane


class Twist(object):
    def __init__(self, obj, frame=Frame.worldXY(), angle=0.0):
        # needs a distance object to act on
        # ev. a plane? origin and normal
        # to rotate query point around
        self.obj = obj
        self.frame = frame
        self.angle = angle

    def get_distance(self, point):
        """
        single point distance function
        """
        plane = Plane(self.frame.point, self.frame.normal)
        plndst = distance_point_plane_signed(point, plane)
        pr = rotate_points([point], plndst/10, self.frame.normal, self.frame.point)
        d = self.obj.get_distance(pr[0])
        return d

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        from compas.geometry import inverse
        import numpy as np

        plane = Plane(self.frame.point, self.frame.normal)
        vp = VolPlane(plane)
        dm = vp.get_distance_numpy(x, y, z)

        m = matrix_from_axis_and_angle(self.frame.normal, 10, self.frame.point)
        mi = inverse(m)
        p = np.array([x, y, z, 1])
        xt, yt, zt, _ = np.dot(mi, p)
        return self.obj.get_distance_numpy(xt, yt, zt)


if __name__ == "__main__":
    from compas_vol.primitives import VolBox
    from compas.geometry import Box

    bx = Box(Frame.worldXY(), 20, 15, 10)
    vb = VolBox(bx, 1.5)

    t = Twist(vb, Frame((0, 0, 0), (1, 0, 0), (0, 0, 1)), 15)

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = t.get_distance((x*0.5, y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
