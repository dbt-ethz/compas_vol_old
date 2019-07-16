import numpy as np
from matplotlib import pyplot as plt
from compas_vol.primitives import VolBox
from compas.geometry import Box, Frame

b = Box(Frame.worldXY(), 5, 4, 3)
vb = VolBox(b, 0.8)

n = 256
x = np.linspace(-3., 3., n)
y = np.linspace(-3., 3., n)
# # z = np.linspace(-3., 3., n//2)
X, Y = np.meshgrid(x, y)

np.vectorize(vb.get_distance)
Z = vb.get_distance(X, Y, 0)
# Z = X * np.sinc(X ** 2 + Y ** 2)

# plt.pcolormesh(X, Y, Z)
# plt.show()
