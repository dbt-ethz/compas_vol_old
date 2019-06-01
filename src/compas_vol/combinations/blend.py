class Blend(object):
    def __init__(self, a=None, b=None, r=1.0):
        self.a = a
        self.b = b
        self.r = r
    
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        e = max(self.r - abs(da-db), 0)
        return min(da,db) - e*e*0.25/self.r

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere()
    b = Box()
    c = Blend(s,b)
    d = c.get_distance(1,2,3)
    print(d)