from scipy.ndimage.filters import gaussian_filter


class Blur(object):
    """
    A `Blur` object is composed of a distance matrix and a radius

    Parameters
    ----------
    distance_matrix :class:`numpy.ndarray` of shape (nx, ny, nz)
        the original distance matrix
    radius : float
        radius of the Gaussian filter kernel
    """
    def __init__(self, distance_matrix, radius=3.0):
        self.distance_matrix = distance_matrix
        self.radius = radius  # ev. pass sigma as argument to get_blurred?

    def get_blurred(self):
        """
        return a blurred copy of the distance matrix
        """
        return gaussian_filter(self.distance_matrix, sigma=self.radius)
