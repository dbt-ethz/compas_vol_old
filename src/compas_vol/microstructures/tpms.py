from math import pi, sin, cos


class TPMS(object):
    """
    Triply Periodic Minimal Surfaces (TMPS)
    """
    def __init__(self, tpmstype='Gyroid', wavelength=1.0):
        self.tpmstype = tpmstype
        self._wavelength = None
        self.wavelength = wavelength
        self._factor = self.wavelength/pi

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def wavelength(self):
        """float: The wavelength of the TPMS."""
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self._wavelength = float(wavelength)

    # ==========================================================================
    # distance function
    # ==========================================================================

    def get_distance(self, point):
        x, y, z = point
        px = x/self._factor
        py = y/self._factor
        pz = z/self._factor

        d = 0
        if self.tpmstype == 'Gyroid':
            d = sin(px)*cos(py) + sin(py)*cos(pz) + sin(pz)*cos(px)
        elif self.tpmstype == 'SchwartzP':
            d = cos(px) + cos(py) + cos(pz)
        elif self.tpmstype == 'Diamond':
            d = (
                sin(px) * sin(py) * sin(pz) +
                sin(px) * cos(py) * cos(pz) +
                cos(px) * sin(py) * cos(pz) +
                cos(px) * cos(py) * sin(pz)
            )
        elif self.tpmstype == 'Neovius':
            d = (3 * cos(px) + cos(py) + cos(pz) +
                 4 * cos(px) * cos(py) * cos(pz))
        elif self.tpmstype == 'Lidinoid':
            d = (0.5 * (sin(2*px) * cos(py) * sin(pz) +
                 sin(2*py) * cos(py) * sin(px) +
                 sin(2*pz) * cos(px) * sin(pz)) -
                 0.5 * (cos(2*px) * cos(2*py) +
                 cos(2*py) * cos(2*pz) +
                 cos(2*pz) * cos(2*px)) + 0.15)
        elif self.tpmstype == 'FischerKoch':
            d = (cos(2*px) * sin(py) * cos(pz) +
                 cos(2*py) * sin(pz) * cos(px) +
                 cos(2*pz) * sin(px) * cos(py))
        return d

    def get_distance_numpy(self, x, y, z):
        import numpy as np

        px = x/self._factor
        py = y/self._factor
        pz = z/self._factor

        if self.tpmstype == 'Gyroid':
            d = np.sin(px)*np.cos(py) + np.sin(py)*np.cos(pz) + np.sin(pz)*np.cos(px)
        elif self.tpmstype == 'SchwartzP':
            d = np.cos(px) + np.cos(py) + np.cos(pz)
        elif self.tpmstype == 'Diamond':
            d = (
                np.sin(px) * np.sin(py) * np.sin(pz) +
                np.sin(px) * np.cos(py) * np.cos(pz) +
                np.cos(px) * np.sin(py) * np.cos(pz) +
                np.cos(px) * np.cos(py) * np.sin(pz)
            )
        elif self.tpmstype == 'Neovius':
            d = (3 * np.cos(px) + np.cos(py) + np.cos(pz) +
                 4 * np.cos(px) * np.cos(py) * np.cos(pz))
        elif self.tpmstype == 'Lidinoid':
            d = (0.5 * (np.sin(2*px) * np.cos(py) * np.sin(pz) +
                 np.sin(2*py) * np.cos(py) * np.sin(px) +
                 np.sin(2*pz) * np.cos(px) * np.sin(pz)) -
                 0.5 * (np.cos(2*px) * np.cos(2*py) +
                 np.cos(2*py) * np.cos(2*pz) +
                 np.cos(2*pz) * np.cos(2*px)) + 0.15)
        elif self.tpmstype == 'FischerKoch':
            d = (np.cos(2*px) * np.sin(py) * np.cos(pz) +
                 np.cos(2*py) * np.sin(pz) * np.cos(px) +
                 np.cos(2*pz) * np.sin(px) * np.cos(py))
        return d


if __name__ == "__main__":
    # from compas.geometry import Point
    import numpy as np
    import matplotlib.pyplot as plt

    b = TPMS(tpmstype='Gyroid', wavelength=5)

    x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    m = b.get_distance_numpy(x, y, z)

    plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    # for y in range(-15, 15):
    #     s = ''
    #     for x in range(-30, 30):
    #         d = b.get_distance(Point(x*0.5, y, 1.))
    #         if d < 0:
    #             s += 'x'
    #         else:
    #             s += '.'
    #     print(s)
