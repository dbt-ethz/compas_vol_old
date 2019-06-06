import math

class Box(object):
    """
    this is the class to create a box
    """
    def __init__(self,length=3.0,width=2.0,height=1.0,radius=0.0):
        self._l = length
        self._w = width
        self._h = height
        self._r = radius

    @classmethod
    def box_from_edge(cls,edge):
        box = cls(edge,edge,edge,0.0)
        return box

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def l(self):
        """float: The length of the box."""
        return self._l

    @l.setter
    def l(self, l):
        self._l = float(l)

    @property
    def w(self):
        """float: The width of the box."""
        return self._w

    @w.setter
    def w(self, w):
        self._w = float(w)

    @property
    def h(self):
        """float: The height of the box."""
        return self._h

    @h.setter
    def h(self, h):
        self._h = float(h)

    @property
    def r(self):
        """float: The radius of the sphere."""
        return self._r

    @r.setter
    def r(self, r):
        self._r = float(r)
  
    # ==========================================================================
    # distance function
    # ==========================================================================

    def get_distance(self,x,y,z):
        dx = abs(x) - (self._l/2.0 - self._r)
        dy = abs(y) - (self._w/2.0 - self._r)
        dz = abs(z) - (self._h/2.0 - self._r)
        inside = max(dx, max(dy,dz)) - self._r
        dx = max(dx,0)
        dy = max(dy,0)
        dz = max(dz,0)
        if inside+self._r<0:
            return inside
        else:
            corner = math.sqrt(dx*dx + dy*dy + dz*dz) - self._r
            return corner

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    b = Box(25,20,15,7)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = b.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)
