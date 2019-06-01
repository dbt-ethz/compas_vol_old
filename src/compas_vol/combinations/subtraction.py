class Subtraction(object):
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b
    
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        return max(da, -db)

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere()
    b = Box()
    c = Subtraction(s,b)
    d = c.get_distance(1,2,3)
    print(d)