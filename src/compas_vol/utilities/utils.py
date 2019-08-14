__all__ = [
    'export_ski_mesh',
    'export_ipv_mesh',
    'get_compas_mesh',
    'export_layer'
    ]


def export_ski_mesh(vs, fs, ns=None, filename='ski_mesh.obj'):
    ve = ['v {} {} {}'.format(v[0], v[1], v[2]) for v in vs]
    if ns is not None:
        ne = ['vn {} {} {}'.format(n[0], n[1], n[2]) for n in ns]
        fe = ['f {0}//{0} {1}//{1} {2}//{2}'.format(f[0]+1, f[1]+1, f[2]+1) for f in fs]
    else:
        ne = None
        fe = ['f {} {} {}'.format(f[0]+1, f[1]+1, f[2]+1) for f in fs]
    with open(filename, 'w') as f:
        f.write('\n'.join(ve))
        f.write('\n')
        if ne is not None:
            f.write('\n'.join(ne))
            f.write('\n')
        f.write('\n'.join(fe))


def export_ipv_mesh(mesh, filename='ipv_mesh.obj'):
    """
    Exports a mesh of type :class:`ipyvolume.widgets.Mesh`
    to an .obj file at specified location.
    """

    import numpy as np

    vs = np.vstack((mesh.x, mesh.y, mesh.z)).T
    # vs = ['v {:.4f} {:.4f} {:.4f}'.format(v[0], v[1], v[2]) for v in vs]
    vs = ['v {} {} {}'.format(v[0], v[1], v[2]) for v in vs]
    fs = ['f {} {} {}'.format(v[0]+1, v[1]+1, v[2]+1) for v in mesh.triangles]

    with open(filename, 'w') as f:
        f.write('\n'.join(vs))
        f.write('\n')
        f.write('\n'.join(fs))


def get_compas_mesh(v, f):
    from compas.datastructures import Mesh
    m = Mesh.from_vertices_and_faces(v, f)
    return m


def export_layer(distfield, resolution, level, filename='layerimage.png'):
    """
    Exports a slice through a distance field as an image.
    """

    import numpy as np
    from skimage import io

    # x, y = np.ogrid[-10:10:resolution+0j, -10:10:resolution+0j]
    y, x = np.ogrid[-10:10:resolution*1j, -10:10:resolution*1j]
    d = distfield.get_distance_numpy(x, y, level)

    # linear gradient
#     d = d - d.min()
#     m = d / d.max()
    # binary image
#     m = (d < 0)*1.0
    # absolute
    d = np.abs(d)
    m = d / d.max()

    io.imsave(filename, m)
    return d


if __name__ == "__main__":
    from compas_vol.primitives import VolBox
    from compas.geometry import Box, Frame

    cb = Box(Frame((0, 0, 0), (1, 0.2, 0.1), (-0.1, 1, 0.2)), 16, 12, 8)
    vb = VolBox(cb, 1.5)
    o = export_layer(vb, 100, 0)
    print(type(o))
