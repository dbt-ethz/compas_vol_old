from compas_vol.primitives import VolSphere, VolBox
from compas_vol.combinations import Subtraction
from compas.geometry import Box, Frame, Point, Sphere, Vector

s = Sphere(Point(5, 6, 0), 9)
b = Box(Frame.worldXY(), 20, 15, 10)
vs = VolSphere(s)
vb = VolBox(b, 2.5)
u = Subtraction(vs, vb)
u2 = eval(str(u))
for y in range(-15, 15):
    s = ''
    for x in range(-30, 30):
        d = u2.get_distance(Point(x*0.5, y, 0))
        if d < 0:
            s += 'x'
        else:
            s += '.'
    print(s)
