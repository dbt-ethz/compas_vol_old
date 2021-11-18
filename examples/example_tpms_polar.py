#imports
import numpy as np
import meshplot as mp
from skimage.measure import marching_cubes
from compas_vol.microstructures import TPMSPolar

#workspace initialization
x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
#voxel dimensions
gx = 28/112
gy = 24/96
gz = 20/80

#VM object
tpmsPol = TPMSPolar(1, 0.4, 1.2, 10.0)

#sampling
dm = tpmsPol.get_distance_numpy(x, y, z)

#generate isosurface
v, f, n, l = marching_cubes(dm, 0, spacing=(gx, gy, gz))

#display mesh
mp.plot(v, f, c=np.array([0,0.57,0.82]), shading={"flat":False, "roughness":0.4, "metalness":0.01, "reflectivity":1.0})