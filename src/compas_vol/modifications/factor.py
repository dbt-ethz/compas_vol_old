class Factor(object):
    def __init__(self, o, f=1.0):
        self.o = o
        self.f = f

    def __repr__(self):
        return "Factor()"
    
    def get_distance(self, point):
        return self.f * self.o.get_distance(point)
    
    def get_distance_numpy(self, x, y, z):
        return self.f * self.o.get_distance_numpy(x,y,z)