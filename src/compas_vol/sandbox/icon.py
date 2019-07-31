if __name__ == "__main__":
    import numpy as np
    from skimage.measure import marching_cubes_lewiner
    import matplotlib.pyplot as plt
    from compas_viewers import Viewer
    from compas.datastructures import Mesh
    from compas_vol.combinations import Union, Subtraction
    from compas_vol.primitives import VolBox, VolSphere
    from compas.geometry import Sphere, Box, Frame

    x, y, z = np.ogrid[-15:15:64j, -15:15:64j, -15:15:64j]
    t1 = VolSphere(Sphere((5, 5, 5), 7))
    b = Box(Frame([-4, 0, 0], [1, 0, 0], [0, 1, 0]), 20, 15, 10)
    t3 = VolBox(b, 3.0)

    u = Union(t1, t3)
    d = u.get_distance_numpy(x, y, z)

    verts, faces, normals, values = marching_cubes_lewiner(d, 0.0)
    print(len(verts), len(faces))
    mesh = Mesh.from_vertices_and_faces(verts, faces)
    
    # view = Viewer()
    # view.mesh = mesh
    # view.show()
    # plt.imshow(np.sin(d[:,:,32]*2), cmap='Greys')
    plt.imshow(d[:,:,32], cmap='coolwarm')
    plt.savefig('/Users/bernham/Desktop/boxsphere_oc.png')
    plt.show()
    mesh.to_obj('/Users/bernham/Desktop/boxsphere.obj')