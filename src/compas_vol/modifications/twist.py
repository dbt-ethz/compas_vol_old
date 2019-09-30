from compas.geometry import Frame


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
        return 0

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        return 0


if __name__ == "__main__":
    pass
