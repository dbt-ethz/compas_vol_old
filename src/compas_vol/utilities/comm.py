from compas.geometry import *  # noqa: F401 F403
from compas_vol.primitives import *  # noqa: F401 F403
from compas_vol.modifications import *  # noqa: F401 F403
from compas_vol.combinations import *  # noqa: F401 F403
from compas_vol.microstructures import *  # noqa: F401 F403

import numpy as np
from skimage.measure import marching_cubes_lewiner


__all__ = [
    'get_vfs_from_tree'
]


def get_vfs_from_tree(tree, bounds, res):
    obj = eval(tree)
    bx = bounds[0]
    by = bounds[1]
    bz = bounds[2]

    # nx = (bx[1]-bx[0])/res

    x, y, z = np.ogrid[bx[0]:bx[1]:bx[2]*1j, by[0]:by[1]:by[2]*1j, bz[0]:bz[1]:bz[2]*1j]
    dm = obj.get_distance_numpy(x, y, z)

    sx = (bx[1]-bx[0])/(bx[2]-1)
    sy = (by[1]-by[0])/(by[2]-1)
    sz = (bz[1]-bz[0])/(bz[2]-1)

    verts, faces, norms, vals = marching_cubes_lewiner(dm, 0.0, spacing=(sx, sy, sz))
    return (verts, faces)


# if __name__ == "__main__":
#     s = VolSphere(Sphere((1, 2, 3), 4))
#     b = VolBox(Box(Frame.worldXY(), 2,3,4), 0.7)
#     u = Union(s,b)
#     print(u)
#     n = eval(str(u))
#     print(n.get_distance((5,4,3)))
