from math import pi, sin, cos
from compas import PRECISION


class TPMS(object):
    """A triply periodic minimal surface (TPMS) is defined by a type and a wavelength.

    Parameters
    ----------
    tpmstype: String
        Type of TPMS. Currently avaliable are Gyroid, SchwartzP, Diamond, Neovius, Lidinoid and FischerKoch.
    wavelength: float
        The wavelength of the trigonometric function.

    Examples
    --------
    >>> a = TPMS(tpmstype='Gyroid', wavelength=5.0)
    """

    def __init__(self, tpmstype=0, wavelength=1.0):
        self.tpmstypes = ['Gyroid', 'SchwartzP', 'Diamond', 'Neovius', 'Lidinoid', 'FischerKoch']
        self.tpmstypesl = [s.lower() for s in self.tpmstypes]
        self._tpmstype = None
        self.tpmstype = tpmstype
        self._wavelength = None
        self.wavelength = wavelength
        self._factor = self.wavelength/pi

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def tpmstype(self):
        return self._tpmstype

    @tpmstype.setter
    def tpmstype(self, tpmstype):
        if type(tpmstype) == str:
            if tpmstype.lower() in self.tpmstypesl:
                self._tpmstype = self.tpmstypesl.index(tpmstype.lower())
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
        self._factor = self.wavelength/pi

    def __repr__(self):
        return 'TPMS({0},{1:.{2}f})'.format(self.tpmstype, self.wavelength, PRECISION[:1])

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
        elif self.tpmstype == 2:  # 'Diamond':
            d = (
                sin(px) * sin(py) * sin(pz) +
                sin(px) * cos(py) * cos(pz) +
                cos(px) * sin(py) * cos(pz) +
                cos(px) * cos(py) * sin(pz)
            )
        elif self.tpmstype == 3:  # 'Neovius':
            d = (3 * cos(px) + cos(py) + cos(pz) +
                 4 * cos(px) * cos(py) * cos(pz))
        elif self.tpmstype == 4:  # 'Lidinoid':
            d = (0.5 * (sin(2*px) * cos(py) * sin(pz) +
                 sin(2*py) * cos(py) * sin(px) +
                 sin(2*pz) * cos(px) * sin(pz)) -
                 0.5 * (cos(2*px) * cos(2*py) +
                 cos(2*py) * cos(2*pz) +
                 cos(2*pz) * cos(2*px)) + 0.15)
        elif self.tpmstype == 5:  # 'FischerKoch':
            d = (cos(2*px) * sin(py) * cos(pz) +
                 cos(2*py) * sin(pz) * cos(px) +
                 cos(2*pz) * sin(px) * cos(py))
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
        # Diamond
        elif self.tpmstype == 2:
            d = (
                np.sin(px) * np.sin(py) * np.sin(pz) +
                np.sin(px) * np.cos(py) * np.cos(pz) +
                np.cos(px) * np.sin(py) * np.cos(pz) +
                np.cos(px) * np.cos(py) * np.sin(pz)
            )
        # Neovius
        elif self.tpmstype == 3:
            d = (3 * np.cos(px) + np.cos(py) + np.cos(pz) +
                 4 * np.cos(px) * np.cos(py) * np.cos(pz))
        # Lidinoid
        elif self.tpmstype == 4:
            d = (0.5 * (np.sin(2*px) * np.cos(py) * np.sin(pz) +
                 np.sin(2*py) * np.cos(py) * np.sin(px) +
                 np.sin(2*pz) * np.cos(px) * np.sin(pz)) -
                 0.5 * (np.cos(2*px) * np.cos(2*py) +
                 np.cos(2*py) * np.cos(2*pz) +
                 np.cos(2*pz) * np.cos(2*px)) + 0.15)
        # FischerKoch
        elif self.tpmstype == 5:
            d = (np.cos(2*px) * np.sin(py) * np.cos(pz) +
                 np.cos(2*py) * np.sin(pz) * np.cos(px) +
                 np.cos(2*pz) * np.sin(px) * np.cos(py))
        # IWP?
        return d