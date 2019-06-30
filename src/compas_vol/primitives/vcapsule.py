from compas.geometry.distance import closest_point_on_segment


__all__ = ['VolCapsule']


class VolCapsule(object):
    def __init__(self, segment, radius):
        self.segment = segment
        self.radius = radius

    def get_distance(self, point):
        p = closest_point_on_segment(point, self.segment)
        return point.distance_to_point(p) - self.radius


if __name__ == "__main__":
    from compas.geometry import Point
    s = ((-9, -9, 0), (9, 9, 0))
    capsule = VolCapsule(s, 5.0)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = capsule.get_distance(Point(x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
