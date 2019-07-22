from compas.geometry import Polyline
from compas.geometry import closest_point_on_polyline_xy
from math import sqrt


class Path(object):
    def __init__(self, polyline, slope=30.0):
        self.polyline = polyline
        self.slope = slope
        # more attributes and properties

    def get_distance(self, point):
        pt = closest_point_on_polyline_xy(point, self.polyline)
        d = sqrt((point.x-pt[0])**2 + (point.y-pt[1])**2 + (point.z-pt[2])**2)
        return d

    def get_distance_numpy(self, x, y):
        # instead of sending 1 point and return 1 distance
        # send all the coordinates and return all the distances
        pass


if __name__ == "__main__":
    import numpy as np
    import random
    import matplotlib.pyplot as plt
    from compas.geometry import Point

    # generate a sequence of some random points
    pts = []
    for i in range(10):
        pts.append([random.random()*40, random.random()*30])

    # create a compas polyline object
    pl = Polyline(pts)

    # create a compas_terrain Path object with the polyline as property
    pth = Path(pl)

    distancemap = np.zeros((30, 40))
    for x in range(40):
        for y in range(30):
            p = Point(x, y, 0)
            d = pth.get_distance(p)
            distancemap[y, x] = d

    plt.imshow(distancemap, cmap='RdBu')
    plt.show()

    """
    # fast numpy alternative would look something like this:
    >>> x, y = np.ogrid[0:40:40j, 0:30:30j]
    >>> distancemap = pth.get_distance_numpy(x, y)
    >>> plt.imshow(distancemap)
    >>> plt.show()
    """
