import numpy as np
import matplotlib.pyplot as plt
from compas_vol.microstructures import TPMSPolar

tpmsPol = TPMSPolar(1, 4.0,3.0, 10.0)

x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
m = tpmsPol.get_distance_numpy(x, y, z)
# print(m)
plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
plt.colorbar()
plt.axis('equal')
plt.show()
