import math

class Sphere(object):

    #@classmethod
    #def from_centre_and_radius(cls,frame,rad):
    #    pass

    def __init__(self,radius=1.0):
        self._r = radius

    # ==========================================================================
    # descriptors
    # ==========================================================================

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
        return math.sqrt(x*x + y*y + z*z) -self.r

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    sp = Sphere(10.5)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = sp.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '.'
        print(s)
