import numpy as np
import matplotlib.pyplot as plt

from compas_vol.primitives import VolSphere
from compas_vol.analysis import Gradient
from compas.geometry import Point, Sphere

s = Sphere(Point(1, 2, 3), 4)
vs = VolSphere(s)

g = Gradient(vs)
print(vs.get_distance(Point(4, 5, 6)))
print(g.get_gradient(Point(5, 2, 3)))

x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
d = g.get_gradient_numpy(x, y, z)

plt.quiver(x, y, d[:, :, 0, 1], d[:, :, 0, 2])
plt.axis('equal')
plt.show()
