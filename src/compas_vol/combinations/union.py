class Union(object):
    def __init__(self, a=None, b=None):
        if type(a)==list:
            self.objs = a
        else:
            self.objs = [a, b]
    
    def get_distance(self,x,y,z):
        ds = [o.get_distance(x,y,z) for o in self.objs]
        return min(ds)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas_vol.primitives import Sphere, Box
    s = Sphere(9)
    b = Box(25,10,10)
    u = Union(s,b)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = u.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)