import numpy as np


# https://stackoverflow.com/questions/41860623/fastest-way-to-fill-numpy-array-with-distances-from-a-point



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
