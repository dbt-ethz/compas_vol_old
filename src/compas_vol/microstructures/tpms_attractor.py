from math import pi, sin, cos
from compas import PRECISION
from compas.geometry import Point
from compas.utilities import remap_values

class TPMSAttractor(object):
    """
    """

    def __init__(self, tpmstype=0, wavelength=1.0):
        self.tpmstypes = ['Gyroid', 'SchwartzP']
        self.tpmstypesl = [s.lower() for s in self.tpmstypes]
        self._tpmstype = None
        self.tpmstype = tpmstype
        self._wavelength = None
        self.wavelength = wavelength
        self._factor = self.wavelength/pi


    # ==========================================================================
    # distance function
    # ==========================================================================

    def get_distance(self, point):
        """
        single point distance function
        """
        x, y, z = point
        px = x/self._factor
        py = y/self._factor
        pz = z/self._factor

        d = 0
        if self.tpmstype == 0:  # 'Gyroid':
            d = sin(px)*cos(py) + sin(py)*cos(pz) + sin(pz)*cos(px)
        elif self.tpmstype == 1:  # 'SchwartzP':
            d = cos(px) + cos(py) + cos(pz)
        return d

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        px = x/self._factor
        py = y/self._factor
        pz = z/self._factor

        d = 0
        # Gyroid
        if self.tpmstype == 0:
            d = np.sin(px) * np.cos(py) + np.sin(py)*np.cos(pz) + np.sin(pz)*np.cos(px)
        # SchwartzP
        elif self.tpmstype == 1:
            d = np.cos(px) + np.cos(py) + np.cos(pz)
        return d



# import Rhino.Geometry as rg

# def remap(val, min, max, minOut, maxOut):
#     if val > max:
#         val = max
#     elif val < min:
#         val = min
    
#     span = max-min
#     spanOut = maxOut - minOut
#     thrust = (val-min)/span
    
#     return minOut + (thrust*spanOut)

# class Attractor(object):
#     """
#     this is the attractor class
#     """
#     def __init__(self,obj,dist,targ):
#         self.obj = obj
#         self.dist = dist
#         self.targ = targ
    
#     def getFactor(self,x,y,z):
#         f = 1
#         newPt = rg.Point3d(x,y,z)
#         if type(self.obj) is list:
#             distances = []
#             factors = []
#             for o in self.obj:
#                 if type(o) is rg.Point3d:
#                     d = rg.Point3d.DistanceTo(o, newPt)
#                     distances.append(d)
#                     f = remap(d, self.dist[0], self.dist[1], self.targ[0], self.targ[1])
#                     factors.append(f)
#                 elif type(o) is rg.Plane:
#                     projectedPt = rg.Plane.ClosestPoint(o, newPt)
#                     d = rg.Point3d.DistanceTo(projectedPt, newPt)
#                     distances.append(d)
#                     f = remap(d, self.dist[0], self.dist[1], self.targ[0], self.targ[1])
#                     factors.append(f)
            
#             m = min(distances)
#             for d,newf in zip(distances, factors):
#                 if d == m:
#                     f = newf
#         else:
#             if type(self.obj) is rg.Point3d:
#                 d = rg.Point3d.DistanceTo(self.obj, newPt)
#                 f = remap(d, self.dist[0], self.dist[1], self.targ[0], self.targ[1])
#             elif type(self.obj) is rg.Plane:
#                 projectedPt = rg.Plane.ClosestPoint(self.obj, newPt)
#                 d = rg.Point3d.DistanceTo(projectedPt, newPt)
#                 f = remap(d, self.dist[0], self.dist[1], self.targ[0], self.targ[1])
        
#         return f