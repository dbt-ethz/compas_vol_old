import numpy as np


# https://stackoverflow.com/questions/41860623/fastest-way-to-fill-numpy-array-with-distances-from-a-point

"""
class Sphere(object):
    def __init__(self, r=1.0, c=[0, 0, 0]):
        self.r = r
        self.c = c

    def get_distance_np(self, x, y, z):
        d = np.sqrt((x - self.c[0])**2 +
                    (y - self.c[1])**2 +
                    (z - self.c[2])**2) - self.r
        return d


class Box(object):
    def __init__(self, a=1.0, b=1.0, c=1.0, r=0.0, p=[0, 0, 0]):
        self.a = a
        self.b = b
        self.c = c
        self.r = r
        self.p = p

    def get_distance_np(self, x, y, z):
        dx = np.abs(x) - (self.a / 2.0 - self.r)
        dy = np.abs(y) - (self.b / 2.0 - self.r)
        dz = np.abs(z) - (self.c / 2.0 - self.r)
        d = np.maximum(dx, np.maximum(dy, dz))
        return d


class Union(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_distance_np(self, x, y, z):
        ad = self.a.get_distance_np(x, y, z)
        bd = self.b.get_distance_np(x, y, z)
        return np.minimum(ad, bd)


class Intersection(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_distance_np(self, x, y, z):
        ad = self.a.get_distance_np(x, y, z)
        bd = self.b.get_distance_np(x, y, z)
        return np.maximum(ad, bd)
"""

if __name__ == "__main__":
    from skimage.measure import marching_cubes_lewiner
    # import matplotlib.pyplot as plt
    from compas_viewers import Viewer
    from compas.datastructures import Mesh
    from compas_vol.combinations import Union, Subtraction
    from compas_vol.primitives import VolBox, VolSphere
    from compas.geometry import Sphere, Box, Frame
    import random

    x, y, z = np.ogrid[-15:15:64j, -15:15:64j, -15:15:64j]
    # d = np.sqrt(x**2 + y**2 + z**2) - 10
    t1 = VolSphere(Sphere((4, 3, 2), 10))
    t2 = VolSphere(Sphere((-4, 2, -1), 12))
    # t3 = Box(25, 20, 15, 0, [3, 4, 5])

    spheres = []
    for i in range(20):
        p = [random.random()*20-10 for _ in range(3)]
        s = Sphere(p, 2 + random.random()*8)
        spheres.append(VolSphere(s))

    u = Union(spheres)
    d = u.get_distance_numpy(x, y, z)

    verts, faces, normals, values = marching_cubes_lewiner(d, 0.0)
    print(len(verts), len(faces))
    mesh = Mesh.from_vertices_and_faces(verts, faces)
    view = Viewer()
    view.mesh = mesh
    view.show()
    # print(d[:5, :5, :5])
    # plt.imshow(d[:,:,15])
    # plt.colorbar()
    # plt.show()
