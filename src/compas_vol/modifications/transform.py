class Transform(object):
    def __init__(self,obj=None, matrix=None):
        self.o = obj
        self.m = matrix
    
    def get_distance(self,x,y,z):
        return 0

if __name__ == "__main__":
    from compas_vol.primitives import Box
    b = Box()
    t = Transform(b)
    d = t.get_distance(1,2,3)
    print(d)