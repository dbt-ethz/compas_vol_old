import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point
# from compas_plotters import MeshPlotter
from compas_viewers import Viewer
from skimage.measure import marching_cubes_lewiner

from compas_vol.primitives import VolBox

frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
b = Box(frame, 25, 20, 15)
vb = VolBox(b, 4.)

# g = np.vectorize(b.get_distance)
# m = np.fromfunction(g, (64, 64, 64))

num = 30
lb = -15.0
ub =  15.0
fact = (ub-lb)/(num-1)
m = np.empty((num, num, num))
for i in range(num):
    for j in range(num):
        for k in range(num):
            x = lb + k*fact
            y = lb + j*fact
            z = lb + i*fact
            v = vb.get_distance(Point(x, y, z))
            m[k, j, i] = v

verts, faces, normals, values = marching_cubes_lewiner(m, 0.0)
mesh = Mesh.from_vertices_and_faces(verts, faces)
print(mesh.summary())

# plotter = MeshPlotter(mesh)

# plotter.draw_faces()
# plotter.show()

view = Viewer()
view.mesh = mesh
view.show()