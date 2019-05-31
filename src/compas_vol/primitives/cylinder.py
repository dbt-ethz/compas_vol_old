import math

class Cylinder(object):
    def __init__(self,radius=1.0,height=2.0):
        self.r = radius
        self.h = height
    
    def get_distance(self,x,y,z):
        d = math.sqrt(x*x + y*y) - self.r
        d = max(d, abs(z) - self.h/2.0)
        return d

if __name__ == "__main__":
    pass