import math

class Torus(object):
    def __init__(self,axisrad=3.0,pipierad=1.0):
        self.R = axisrad
        self.r = pipierad
    
    def get_distance(self,x,y,z):
        lxy = math.sqrt(x*x + y*y)
        l2 = math.sqrt((lxy-self.R)**2 + z*z)
        return l2 - self.r

if __name__ == "__main__":
    t = Torus(15,8)
    for y in range(-30,30):
        s = ''
        for x in range(-60,60):
            d = t.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '-'
        print(s)