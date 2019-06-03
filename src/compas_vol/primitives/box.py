import math

class Box(object):
    def __init__(self,length=3.0,width=2.0,height=1.0,radius=0.0):
        self.l = length
        self.w = width
        self.h = height
        self.r = radius
    
    def get_distance(self,x,y,z):
        dx = abs(x) - (self.l/2.0 - self.r)
        dy = abs(y) - (self.w/2.0 - self.r)
        dz = abs(z) - (self.h/2.0 - self.r)
        inside = max(dx, max(dy,dz)) - self.r
        dx = max(dx,0)
        dy = max(dy,0)
        dz = max(dz,0)
        if inside+self.r<0:
            return inside
        else:
            corner = math.sqrt(dx*dx + dy*dy + dz*dz) - self.r
            return corner

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
