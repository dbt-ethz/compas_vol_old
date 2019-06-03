class Shell(object):
    """
    creates a shell of thickness d
    side factor s:
        1.0 > inside
        0.5 > half half
        0.0 > outside
    """

    def __init__(self, obj, d=1.0, s=0.0):
        self.o = obj
        self.d = d
        self.s = s

    def get_distance(self,x,y,z):
        do = self.o.get_distance(x,y,z)
        return abs(do + (self.s-0.5)*self.d)-self.d/2.0

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    from compas_vol.combinations import Union
    
    s = Sphere(9)
    b = Box(25,10,10)
    u = Union(s,b)
    sh = Shell(u,2.5,0.5)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = sh.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)