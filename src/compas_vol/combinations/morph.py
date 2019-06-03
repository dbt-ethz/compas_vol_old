class Morph(object):
    def __init__(self, a=None, b=None, f=0.5):
        self.a = a
        self.b = b
        self.f = f
    
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        return (1.0-self.f)*da + self.f*db

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere(9)
    b = Box(25,10,10)
    u = Morph(s,b,0.5)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = u.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)