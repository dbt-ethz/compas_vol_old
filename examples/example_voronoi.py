#imports
import numpy as np
import meshplot as mp
from skimage.measure import marching_cubes
from compas.geometry import Point
from compas_vol.microstructures import Voronoi

#workspace initialization
x, y, z = np.ogrid[-30:30:100j, -30:30:100j, -30:30:100j]
#voxel dimensions
gx = 60/100
gy = 60/100
gz = 60/100

#pts generation
nbr_pts = 16
coordinates = np.random.uniform(-30, 30, (nbr_pts,3))
pts = [Point(px,py,pz) for (px,py,pz) in coordinates]

#VM object
v = Voronoi(pts, thickness=2.0)

#sampling
dm = v.get_distance_numpy(x, y, z)

#generate isosurface
v, f, n, l = marching_cubes(dm, 0, spacing=(gx, gy, gz))

#display mesh
mp.plot(v, f, c=np.array([0,0.57,0.82]), shading={"flat":True, "roughness":0.4, "metalness":0.01, "reflectivity":1.0})