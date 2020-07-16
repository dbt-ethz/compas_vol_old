import math
from compas_vol.microstructures import TPMS
from compas.geometry import Point
from compas import PRECISION


class TPMSPolar(object):
    """
    --> To fill in
    --------
    Examples
    --------
    >>> from compas_vol.microstructure import TPMSPolar
    --> To fill in

    """

    def __init__(self, TPMStype=0, waveLength=1.0, thickness=0.1, polar=1.0):
        self.TPMStype = TPMStype
        self.tpmstypes = ['gyroid', 'schwartzp', 'diamond', 'neovius', 'lidinoid', 'fischerkoch']
        self._tpmstype = None
        self.waveLength = waveLength
        self._waveLength = None
        self.thickness = thickness
        self.polar = polar
        self.tpms = self.createTPMSFunction(self.TPMStype, self.waveLength)


    def createTPMSFunction(self, type, waveLength):
        tpms = TPMS(type, waveLength)
        return tpms

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def tpmstype(self):
        return self._tpmstype

    @tpmstype.setter
    def tpmstype(self, tpmstype):
        if type(tpmstype) == str:
            if tpmstype.lower() in self.tpmstypes:
                self._tpmstype = self.tpmstypes.index(tpmstype.lower())
            else:
                self._tpmstype = 0
        elif type(tpmstype) == int:
            self._tpmstype = max(0, min(tpmstype, len(self.tpmstypes) - 1))

    @property
    def wavelength(self):
        """float: The wavelength of the TPMS."""
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self._wavelength = float(wavelength)
        # self._factor = self.wavelength/pi

    def __repr__(self):
        return 'TPMS({0},{1:.{2}f})'.format(self.TPMStype, self.wavelength, PRECISION[:1])


    # ==========================================================================
    # distance function
    # ==========================================================================


    def get_distance(self, point):
        """
        single point distance function
        """
        x, y, z = point

        px = np.sqrt(x**2 + y**2)
        py = np.arctan2(y, x)*self.polar
        pz = z

        d = 0
        if self.TPMStype == 0:  # 'Gyroid':
            d = math.sin(px)*math.cos(py) + math.sin(py)*math.cos(pz) + math.sin(pz)*math.cos(px)
        elif self.TPMStype == 1:  #  'SchwartzP':
            d = math.cos(px) + math.cos(py) + math.cos(pz)
        elif self.TPMStype == 2:  #  'Diamond':
            d = (
                math.sin(px) * math.sin(py) * math.sin(pz) +
                math.sin(px) * math.cos(py) * math.cos(pz) +
                math.cos(px) * math.sin(py) * math.cos(pz) +
                math.cos(px) * math.cos(py) * math.sin(pz)
            )
        elif self.TPMStype == 3:  #  'Neovius':
            d = (3 * math.cos(px) + math.cos(py) + math.cos(pz) +
                 4 * math.cos(px) * math.cos(py) * math.cos(pz))
        elif self.TPMStype == 4:  #  'Lidinoid':
            d = (0.5 * (math.sin(2*px) * math.cos(py) * math.sin(pz) +
                 math.sin(2*py) * math.cos(py) * math.sin(px) +
                 math.sin(2*pz) * math.cos(px) * math.sin(pz)) -
                 0.5 * (math.cos(2*px) * math.cos(2*py) +
                 math.cos(2*py) * math.cos(2*pz) +
                 math.cos(2*pz) * math.cos(2*px)) + 0.15)
        elif self.TPMStype == 5:  #  'FischerKoch':
            d = (math.cos(2*px) * math.sin(py) * math.cos(pz) +
                 math.cos(2*py) * math.sin(pz) * math.cos(px) +
                 math.cos(2*pz) * math.sin(px) * math.cos(py))
        return d
    

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        px = np.sqrt(x**2 + y**2)
        py = np.arctan2(y, x)*self.polar
        pz = z

        d = 0
        if self.TPMStype == 0: #'Gyroid':
            d = np.sin(px)*np.cos(py) + np.sin(py)*np.cos(pz) + np.sin(pz)*np.cos(px)
        elif self.TPMStype == 1: #'SchwartzP':
            d = np.cos(px) + np.cos(py) + np.cos(pz)
        elif self.TPMStype == 2: #'Diamond':
            d = (
                np.sin(px) * np.sin(py) * np.sin(pz) +
                np.sin(px) * np.cos(py) * np.cos(pz) +
                np.cos(px) * np.sin(py) * np.cos(pz) +
                np.cos(px) * np.cos(py) * np.sin(pz)
            )
        elif self.TPMStype == 3: #'Neovius':
            d = (3 * np.cos(px) + np.cos(py) + np.cos(pz) +
                 4 * np.cos(px) * np.cos(py) * np.cos(pz))
        elif self.TPMStype == 4: #'Lidinoid':
            d = (0.5 * (np.sin(2*px) * np.cos(py) * np.sin(pz) +
                 np.sin(2*py) * np.cos(py) * np.sin(px) +
                 np.sin(2*pz) * np.cos(px) * np.sin(pz)) -
                 0.5 * (np.cos(2*px) * np.cos(2*py) +
                 np.cos(2*py) * np.cos(2*pz) +
                 np.cos(2*pz) * np.cos(2*px)) + 0.15)
        elif self.TPMStype == 5: #'FischerKoch':
            d = (np.cos(2*px) * np.sin(py) * np.cos(pz) +
                 np.cos(2*py) * np.sin(pz) * np.cos(px) +
                 np.cos(2*pz) * np.sin(px) * np.cos(py))
        return d - self.thickness/2.0
        

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    tpmsPol = TPMSPolar(1, 4.0,3.0, 10.0)

    x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]
    m = tpmsPol.get_distance_numpy(x, y, z)
    # print(m)
    plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    plt.colorbar()
    plt.axis('equal')
    plt.show()