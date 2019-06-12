from compas.geometry import Box
from math import sqrt

def get_dist(b,x,y,z):
    dx = abs(x) - (b.l/2.0 - b.r)
    dy = abs(y) - (b.w/2.0 - b.r)
    dz = abs(z) - (b.h/2.0 - b.r)
    inside = max(dx, max(dy,dz)) - b.r
    dx = max(dx,0)
    dy = max(dy,0)
    dz = max(dz,0)
    if inside+b._r<0:
        return inside
    else:
        corner = sqrt(dx*dx + dy*dy + dz*dz) - b.r
        return corner