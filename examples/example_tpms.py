# from compas.geometry import Point
import numpy as np
import matplotlib.pyplot as plt
from compas_vol.microstructures import TPMS

b = TPMS(tpmstype='schwartzP', wavelength=5)
print(b)

x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

m = b.get_distance_numpy(x, y, z)

plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
plt.colorbar()
plt.axis('equal')
plt.show()

# for y in range(-15, 15):
#     s = ''
#     for x in range(-30, 30):
#         d = b.get_distance(Point(x*0.5, y, 1.))
#         if d < 0:
#             s += 'x'
#         else:
#             s += '.'
#     print(s)
