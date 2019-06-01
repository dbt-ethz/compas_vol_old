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
    s = Sphere()
    b = Box()
    c = Morph(s,b,0.2)
    d = c.get_distance(1,2,3)
    print(d)