import math
import matplotlib.pyplot as plt
import numpy as np
import time

from compas_vol.primitives import VolExtrusion
from compas.geometry import Point, Frame

polyline = []
a = math.pi*2/10
r = 10
for i in range(10):
    tr = r
    if i % 2:
        tr = 5
    x = tr*math.cos(i*a)
    y = tr*math.sin(i*a)
    polyline.append((x, y, 0))
polyline.append(polyline[0])

ve = VolExtrusion(polyline, height=20, frame=Frame((1, 2, 3), (1, 0.3, 0.1), (-0.4, 1, 0.3)))

x, y, z = np.ogrid[-30:30:60j, -15:15:60j, -15:15:60j]

start = time.time()
d = ve.get_distance_numpy(x, y, z)
end = time.time()
print(end-start)
m = np.tanh(d[:, :, 30].T)
plt.imshow(m, cmap='Greys', interpolation='nearest')
plt.colorbar()
plt.axis('equal')
plt.show()

m = np.empty((60, 30))
for y in range(-15, 15):
    s = ''
    for x in range(-30, 30):
        start2 = time.time()
        d = ve.get_distance(Point(x * 0.5, -y, 0))
        end2 = time.time()
        m[x + 30, y + 15] = d
        if d < 0:
            s += 'O'
        else:
            s += '.'
    print(s)
print(end2-start2)
plt.imshow(m, cmap='RdBu')
plt.colorbar()
plt.show()