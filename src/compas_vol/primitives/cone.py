from math import atan
from math import cos
from math import sin
from math import sqrt


class Cone(object):
    def __init__(self, r=1.0, h=1.0):
        self._r = r
        self._h = h

    def get_distance(self, x, y, z):
        theta = atan(self._r/self._h)
        dxy = sqrt(x*x + y*y)
        d = max(dxy*cos(theta) - abs(z)*sin(theta), z-self._h, -z)
        return d


'''
IQ
float sdCone( vec3 p, vec2 c )
{
    // c must be normalized
    float q = length(p.xy);
    return dot(c,vec2(q,p.z));
}
'''

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    c = Cone(10, 5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = c.get_distance(x * 0.5, y, 2.5)
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
