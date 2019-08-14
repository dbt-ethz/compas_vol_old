import random
import time

import mcubes
import numpy as np
from skimage.measure import marching_cubes_lewiner

from compas.datastructures import Mesh
from compas.geometry import Point, Sphere
from compas_vol.combinations import Union
from compas_vol.primitives import VolSphere
from compas_vol.utilities import export_ski_mesh

pt = time.time()
spheres = []
for i in range(30):
    p = Point(random.random()*100, random.random()*100, random.random()*100)
    s = VolSphere(Sphere(p, 7+random.random()*21))
    spheres.append(s)

u = Union(spheres)

print('create objects', time.time() - pt)
pt = time.time()

x, y, z = np.ogrid[0:100:100j, 0:100:100j, 0:100:100j]
d = u.get_distance_numpy(x, y, z)

print('calculate distances', time.time() - pt)
pt = time.time()

# pymcubes
# verts1, faces1 = mcubes.marching_cubes(d, 0.0)

# print('pymcubes', time.time() - pt)
# pt = time.time()

# skimage
verts, faces, normals, values = marching_cubes_lewiner(d, 0.0)
export_ski_mesh(verts, faces, normals, '/Users/bernham/Desktop/somesphereshizzle.obj')

print('skimage', time.time() - pt)
pt = time.time()
# skimage is 4-5 times faster than pymcubes!

# mesh = Mesh.from_vertices_and_faces(verts, faces)

# print('create compas mesh', time.time() - pt)
# pt = time.time()

# mesh.to_obj('/Users/bernham/Desktop/spheres.obj')

# print('export mesh', time.time() - pt)
