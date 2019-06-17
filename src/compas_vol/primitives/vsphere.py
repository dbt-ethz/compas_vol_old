from compas.geometry._primitives import Sphere, Frame, Point
from compas.geometry.xforms import Transformation
from math import sqrt

class VolSphere(object):
    def __init__(self, point=Point(0,0,0), radius=1.0):
        self._sph = None
        self.sph = Sphere(point,radius)
    @property
    def sph(self):
        return self._sph

    @sph.setter
    def sph(self, sphere):
        self._sph = sphere

    def get_distance(self,x,y,z):
        pass

if __name__ == "__main__":
    pass