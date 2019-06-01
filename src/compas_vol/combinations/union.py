class Union(object):
    def __init__(self, a=None, b=None):
        if type(a)==list:
            self.objs = a
        else:
            self.objs = [a, b]
    
    def get_distance(self,x,y,z):
        ds = [o.get_distance(x,y,z) for o in self.objs]
        return min(ds)

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere()
    b = Box()
    c = Union(s,b)
    d = c.get_distance(1,2,3)
    print(d)