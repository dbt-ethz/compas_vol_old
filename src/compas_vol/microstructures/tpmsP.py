import math
from compas_vol.microstructures import TPMS
from compas.geometry import Point


class TPMSPolar(object):
    """
    --> To fill in
    --------
    Examples
    --------
    >>> from compas_vol.microstructure import TPMSPolar
    --> To fill in

    """

    def __init__(self, TPMStype=0, waveLength=1.0, polar=1.0):
        self.TPMStype = TPMStype
        self.waveLength = waveLength / (2*math.pi)
        self.polar = polar
        self.tpms = self.createTPMSFunction(self.TPMStype, self.waveLength)

    
    # ==========================================================================
    # descriptors
    # ==========================================================================

    def createTPMSFunction(self, type, waveLength):
        tpms = TPMS(type, waveLength)
        return tpms


    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            pt = Point(*point)
        else:
            pt = point

        px = math.sqrt(pt.x * pt.x + pt.y * pt.y)
        py = math.atan2(pt.y, pt.x)*self.polar
        pz = pt.z
        return (px, py, pz)
    

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        p = np.array([x, y, z, 1])

        npx = np.sqrt(p[0]**2 + p[1]**2)
        npy = np.arctan2(p[1], p[0])*self.polar
        npz = p[2]
        return np.asarray([npx,npy,npz])



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    pt = Point(0,0,0)
    tpmsPol = TPMSPolar(1, 7.0, 2.5)

    d = tpmsPol.get_distance(pt)


    # x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
    # m = tpmsPol.get_distance_numpy(x, y, z)
    # print(m)
    # plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    # plt.colorbar()
    # plt.axis('equal')
    # plt.show()











