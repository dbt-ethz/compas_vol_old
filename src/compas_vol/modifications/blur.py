from scipy.ndimage.filters import gaussian_filter


class Blur(object):
    def __init__(self, distance_matrix, radius=3.0):
        self.distance_matrix = distance_matrix
        self.radius = radius

    def get_blurred(self):
        return gaussian_filter(self.distance_matrix, sigma=self.radius)


if __name__ == "__main__":
    from compas_vol.primitives import VolBox
    from compas_vol.combinations import Union
    from compas.geometry import Box, Frame
    import numpy as np
    import matplotlib.pyplot as plt
    import random

    boxes = []
    for i in range(10):
        pt = [random.random()*8-4 for _ in range(3)]
        xa = [random.random() for _ in range(3)]
        ya = [random.random() for _ in range(3)]
        b = Box(Frame(pt, xa, ya), 4, 3, 2)
        vb = VolBox(b)
        boxes.append(vb)
    u = Union(boxes)

    x, y, z = np.ogrid[-5:5:70j, -5:5:70j, -5:5:50j]

    m = u.get_distance_numpy(x, y, z)
    plt.subplot(1, 2, 1)
    plt.imshow(m[:, :, 25], cmap='RdBu')

    b = Blur(m)
    o = b.get_blurred()
    plt.subplot(1, 2, 2)
    plt.imshow(o[:, :, 25], cmap='RdBu')
    plt.show()
