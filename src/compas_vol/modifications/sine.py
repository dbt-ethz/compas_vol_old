from math import sin

class Sine(object):
    def __init__(self, o):
        self.o = o
        self.f = f

    def __repr__(self):
        return "Sine()"
    
    def get_distance(self, point):
        return sin(self.o.get_distance(point))
    
    def get_distance_numpy(self, x, y, z):
        import numpy as np
        return np.sin(self.o.get_distance_numpy(x,y,z))