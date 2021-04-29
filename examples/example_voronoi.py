# from compas.geometry import Point
import numpy as np
import matplotlib.pyplot as plt
from compas.geometry import Pointcloud, Point
from compas_vol.microstructures import Voronoi

dim = 300
points = Pointcloud.from_bounds(dim, dim, 0, 66)
b = Voronoi(points=points, thickness=2.5)

# b.get_distance((2,3,4))
#x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

#m = b.get_distance_numpy(x, y, z)

# plt.imshow(m[:, :, 25].T, cmap='RdBu')
# plt.colorbar()
# plt.axis('equal')
# plt.show()

m = np.empty((dim, dim))
for y in range(dim):
    s = ''
    for x in range(dim):
        d = b.get_distance(Point(x, y, 0))
        m[y, x] = min(d, 25)
        #print(d)
    #     if d < 0:
    #         s += 'x'
    #     else:
    #         s += '.'
    # print(s)
# print(m.min(), m.max())
plt.imshow(m, cmap='gnuplot2')
plt.show()
