def export_mesh(mesh, filename):
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


def export_layer(distfield, resolution, level):
    """
    Exports a slice through a distance field as an image.
    """

    import numpy as np

    # x, y = np.ogrid[-10:10:resolution+0j, -10:10:resolution+0j]
    y, x = np.ogrid[-10:10:10j, -10:10:10j]

    return (x, y)


if __name__ == "__main__":
    o = export_layer(10, 5)
    print(type(o[0]))
