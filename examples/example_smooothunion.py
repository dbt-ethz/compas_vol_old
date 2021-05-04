from compas_vol.primitives import VolSphere, VolBox
from compas_vol.combinations import SmoothUnion
from compas.geometry import Box, Frame, Point, Sphere
import numpy as np
import matplotlib.pyplot as plt

s = Sphere(Point(4, 5, 0), 7)
b = Box(Frame.worldXY(), 20, 15, 10)
vs = VolSphere(s)
vb = VolBox(b, 2.5)
u = SmoothUnion(vs, vb, 6.5)
# for y in range(-15, 15):
#     s = ''
#     for x in range(-30, 30):
#         d = u.get_distance(Point(x*0.5, y, 0))
#         if d < 0:
#             s += 'x'
#         else:
#             s += '.'
#     print(s)

x, y, z = np.ogrid[-15:15:100j, -15:15:100j, -15:15:100j]
d = u.get_distance_numpy(x, y, z)
m = d[:, :, 50].T
plt.imshow(-np.tanh(m*5), cmap='Greys')
# plt.colorbar()
plt.show()
