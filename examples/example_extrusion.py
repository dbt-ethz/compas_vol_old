#imports
import numpy as np
import meshplot as mp
from skimage.measure import marching_cubes
from compas_vol.primitives import VolExtrusion
from compas.geometry import Frame

#workspace initialization
x, y, z = np.ogrid[-30:30:100j, -15:15:100j, -15:15:100j]
#voxel dimensions
gx = 60/100
gy = 30/100
gz = 30/100

#lines generation
polyline = []
a = np.pi*2/10
r = 10
for i in range(10):
    tr = r
    if i % 2:
        tr = 5
    xp = tr*np.cos(i*a)
    yp = tr*np.sin(i*a)
    polyline.append((xp, yp, 0))
polyline.append(polyline[0])

#VM object
ve = VolExtrusion(polyline, height=5, frame=Frame((1, 2, 3), (1, 0.3, 0.1), (-0.4, 1, 0.3)))

#sampling
dm = ve.get_distance_numpy(x, y, z)

#generate isosurface
v, f, n, l = marching_cubes(dm, 0, spacing=(gx, gy, gz))

#display mesh
mp.plot(v, f, c=np.array([0,0.57,0.82]), shading={"flat":True, "roughness":0.4, "metalness":0.01, "reflectivity":1.0})