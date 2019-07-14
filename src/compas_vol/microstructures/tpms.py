from math import pi, sin, cos


class TPMS(object):
    def __init__(self, tpmstype='Gyroid', wavelength=1.0):
        self._t = tpmstype
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
        if self._t == 'Gyroid':
            d = sin(px)*cos(py) + sin(py)*cos(pz) + sin(pz)*cos(px)
        elif self._t == 'SchwartzP':
            d = cos(px) + cos(py) + cos(pz)
        elif self._t == 'Diamond':
            d = (
                sin(px) * sin(py) * sin(pz) +
                sin(px) * cos(py) * cos(pz) +
                cos(px) * sin(py) * cos(pz) +
                cos(px) * cos(py) * sin(pz)
            )

        return d


if __name__ == "__main__":
    from compas.geometry import Point

    b = TPMS(tpmstype='Diamond', wavelength=5)
    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = b.get_distance(Point(x*0.5, y, 1.))
            if d < 0:
                s += 'x'
            else:
                s += '·'
        print(s)
