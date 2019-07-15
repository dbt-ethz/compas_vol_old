import numpy as np


# https://stackoverflow.com/questions/41860623/fastest-way-to-fill-numpy-array-with-distances-from-a-point


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
        d = np.sqrt((x - self.c[0])**2 +
                    (y - self.c[1])**2 +
                    (z - self.c[2])**2) - self.r
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


if __name__ == "__main__":
    from skimage.measure import marching_cubes_lewiner
    # import matplotlib.pyplot as plt
    from compas_viewers import Viewer
    from compas.datastructures import Mesh

    x, y, z = np.ogrid[-15:15:50j, -15:15:50j, -15:15:50j]
    print(x[:10])
    # d = np.sqrt(x**2 + y**2 + z**2) - 10
    t1 = Sphere(10, [-4, -3, -2])
    t2 = Sphere(12, [4, 5, 6])

    u = Intersection(t1, t2)
    d = u.get_distance_np(x, y, z)

    verts, faces, normals, values = marching_cubes_lewiner(d, 0.0)
    mesh = Mesh.from_vertices_and_faces(verts, faces)
    view = Viewer()
    view.mesh = mesh
    view.show()
    # print(d[:5, :5, :5])
    # plt.imshow(d[:,:,15])
    # plt.colorbar()
    # plt.show()
