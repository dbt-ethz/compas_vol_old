import math

class Cylinder(object):
    def __init__(self,radius=1.0,height=2.0):
        self.r = radius
        self.h = height
    
    def get_distance(self,x,y,z):
        d = math.sqrt(x*x + y*y) - self.r
        d = max(d, abs(z) - self.h/2.0)
        return d

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    c = Cylinder(10,5)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = c.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)
