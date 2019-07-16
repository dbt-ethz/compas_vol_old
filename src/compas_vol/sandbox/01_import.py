import compas_vol.primitives as pr
from compas.geometry import Box, Frame

b = Box(Frame.worldXY(), 5, 4, 3)
vb = pr.VolBox(b, 0.8)

print(vb)