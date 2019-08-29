from compas.geometry.xforms import Transformation
from compas.geometry import Point

class Transform(object):
    def __init__(self,obj=None, matrix=None):
        self.o = obj
        self.m = matrix
    
    def get_distance(self,x,y,z):
        p = Point(x,y,z)
        i = self.m.inverse()
        p.transform(i)
        return self.o.get_distance(p.x,p.y,p.z)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas_vol.primitives import Box
    from compas.geometry import Frame

    b = Box(25,20,15,5)
    #f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    f1 = Frame([0,0,0],[1,0.2,0],[-0.2,1,0])
    T = Transformation.from_frame(f1)
    # alternatively: from_matrix, from_list
    t = Transform(b,T)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = t.get_distance(x*0.5,-y,0)
            if d<0:
                s += 'x'
            else:
                s += '.'
        print(s)