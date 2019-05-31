import math

class Sphere(object):
    def __init__(self,radius=1.0):
        self.r = radius
    
    def get_distance(self,x,y,z):
        return math.sqrt(x*x + y*y + z*z) -self.r

if __name__ == "__main__":
    s = Sphere(2.4)
    d = s.get_distance(1,2,3)
    print(d)