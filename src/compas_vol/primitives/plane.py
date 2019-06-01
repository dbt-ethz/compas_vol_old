from compas.geometry.basic import dot_vectors
from compas.geometry import Vector

class Plane(object):
    def __init__(self,nx=0.0,ny=0.0,nz=1.0,distance=0.0):
        self.n = Vector(nx,ny,nz)
        self.d = distance
    
    def get_distance(self,x,y,z):
        dp = dot_vectors(Vector(x,y,z), self.n)
        return -(dp+self.d)

if __name__ == "__main__":
    p = Plane(1,2,3,4)
    d = p.get_distance(4,3,2)
    print(d)