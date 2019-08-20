class Heart(object):
    def __init__(self, size):
        self.size = size

    def get_distance(self, point):
        x, y, z = point
        x /= self.size * 0.43
        y /= self.size * 0.43
        z /= self.size * 0.43
        res = 320 * ((-x**2 * z**3 - 9*y**2 * z**3/80) +
                     (x**2 + 9*y**2/4 + z**2-1)**3)
        return res

    def get_distance_numpy(self, x, y, z):
        raise NotImplementedError


if __name__ == "__main__":
    h = Heart(20)

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = h.get_distance((x * 0.5, 0, -y))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
