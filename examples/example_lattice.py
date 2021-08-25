#imports
import numpy as np
import meshplot as mp
from skimage.measure import marching_cubes
from compas.geometry import Frame
from compas_vol.microstructures import Lattice

#workspace initialization
x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
#voxel dimensions
gx = 28/112
gy = 24/96
gz = 20/80

#VM object
lat = Lattice(7, 5.0, 0.5, frame=Frame((1, 0, 0), (1, 0.2, 0.1), (-0.3, 1, 0.2)))

#sampling
m = lat.get_distance_numpy(x, y, z)

#generate isosurface
v, f, n, l = marching_cubes(m, 0, spacing=(gx, gy, gz))

#display mesh
mp.plot(v, f, c=np.array([0, 0.57, 1.0]), shading={"flat":False, "roughness":0.4, "metalness":0.01, "reflectivity":1.0})