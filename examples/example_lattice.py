import numpy as np
import matplotlib.pyplot as plt
from compas.geometry import Point, Vector, Frame
from compas_vol.microstructures import Lattice

lat = Lattice(7, 5.0, 0.5)
lat.frame = Frame((1, 0, 0), (1, 0.2, 0.1), (-0.3, 1, 0.2))

print(lat.typenames, lat.lattice_type)
print(lat)
lat2 = eval(str(lat))

x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

m = lat2.get_distance_numpy(x, y, z)

# num = 200
# m = np.empty((num, num))
# for r in range(num):
#     for c in range(num):
#         m[r, c] = lat.get_distance((c, r, 10))

plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
plt.colorbar()
plt.axis('equal')
plt.show()
