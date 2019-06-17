from compas.geometry._primitives import Plane, Point


class VolPlane(object):
    def __init__(self, plane):
        self.plane = plane
    
    def get_distance(self, point):
        return point.distance_to_plane(self.plane)


if __name__ == "__main__":
    p = VolPlane(Plane((0, 2, 0), (1, 1, 1)))
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = p.get_distance(Point(x * 0.5, 0, -y))
            if abs(d) < 0.5:
                s += 'x'
            else:
                s += '·'
        print(s)
