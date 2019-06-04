from compas.geometry.basic import dot_vectors
from compas.geometry import Vector

# maybe replace with compas Frame?

class Plane(object):
    def __init__(self,nx=0.0,ny=0.0,nz=1.0,distance=0.0):
        self.n = Vector(nx,ny,nz)
        self.d = distance
    
    def get_distance(self,x,y,z):
        dp = dot_vectors(Vector(x,y,z), self.n)
        return -(dp+self.d)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    p = Plane(1,2,3,4)
    for y in range(-15,15):
        s = ''
        for x in range(-30,30):
            d = p.get_distance(x*0.5,y,0)
            if d<0:
                s += 'x'
            else:
                s += '·'
        print(s)
