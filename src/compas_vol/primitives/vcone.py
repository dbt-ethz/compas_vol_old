class VolCone(object):
    def __init__(self, cone):
        self.cone = cone

    def get_distance(self, point):
        raise NotImplementedError

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":
    from compas.geometry import Cone, Circle, Plane

    c = Cone(Circle(Plane((0, 0, 0), (0, 0, 1)), 3.), 4.)
    vc = VolCone(c)
