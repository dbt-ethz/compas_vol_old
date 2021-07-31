import numpy as np
import meshplot as mp
import ipyvolume as ipv
import matplotlib.pyplot as plt
from compas_vol.microstructures import TPMS

x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
b = TPMS(tpmstype='schwartzP', wavelength=5)
m = b.get_distance_numpy(x, y, z)

ipv_mesh = ipv.plot_isosurface(m, 0.0)
print(ipv_mesh.keys)
# v = np.empty((ipv_mesh.x.size,3))
# v[:,0], v[:,1], v[:,2] = ipv_mesh.x, ipv_mesh.y, ipv_mesh.z
# f = ipv_mesh.triangles
# mp.plot(v, f)

# plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
# plt.colorbar()
# plt.axis('equal')
# plt.show()

# for y in range(-15, 15):
#     s = ''
#     for x in range(-30, 30):
#         d = b.get_distance(Point(x*0.5, y, 1.))
#         if d < 0:
#             s += 'x'
#         else:
#             s += '.'
#     print(s)
