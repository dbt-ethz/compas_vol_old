#imports
import numpy as np
import meshplot as mp
from skimage.measure import marching_cubes
from compas_vol.combinations import Morph
from compas_vol.primitives import VolSphere, VolBox
from compas.geometry import Box, Frame, Point, Sphere

#workspace initialization
x, y, z = np.ogrid[-30:30:100j, -30:30:100j, -30:30:100j]
#voxel dimensions
gx = 60/100
gy = 60/100
gz = 60/100

#CSG tree
s = Sphere(Point(5, 6, 0), 9)
b = Box(Frame.worldXY(), 20, 15, 10)
vs = VolSphere(s)
vb = VolBox(b, 2.5)
u = Morph(vs, vb, 0.5)

#sampling
dm = u.get_distance_numpy(x, y, z)

#generate isosurface
v, f, n, l = marching_cubes(dm, 0, spacing=(gx, gy, gz))

#display mesh
mp.plot(v, f, c=np.array([0,0.57,0.82]), shading={"flat":False, "roughness":0.4, "metalness":0.01, "reflectivity":1.0})
