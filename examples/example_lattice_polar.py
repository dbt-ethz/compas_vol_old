import numpy as np
import matplotlib.pyplot as plt
from compas_vol.microstructures import LatticePolar
# from compas.geometry import Vector, Frame

lat = LatticePolar(1, 7.0, 2.5, 8)

x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
m = lat.get_distance_numpy(x, y, z)
plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
plt.colorbar()
plt.axis('equal')
plt.show()

# print(lat.ltype)
# #lat.frame = Frame((1, 0, 0), (1, 0.2, 0.1), (-0.3, 1, 0.2))
# for y in range(-15, 15):
#     s = ''
#     for x in range(-30, 30):
#         d = lat.get_distance(Point(x*0.5, y, 2))
#         #print(d)
#         if d < 0:
#             s += 'x'
#         else:
#             s += '.'
#     print(s)
