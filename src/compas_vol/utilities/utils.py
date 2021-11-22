import math
import random
#import numpy as np

__all__ = [
    'export_ski_mesh',
    'export_ipv_mesh',
    'get_compas_mesh',
    'export_layer',
    'get_random_vector_2D',
    'get_random_vector_3D',
    'get_iso_mesh',
    'get_iso_vfs',
    'add_cube'
]


def get_iso_mesh(distobj, bounds):
    # for RPC
    from skimage.measure import marching_cubes_lewiner
    import numpy as np
    from compas_vol.primitives import VolBox
    from compas.geometry import Box

    bx = bounds[0]
    by = bounds[1]
    bz = bounds[2]
    x, y, z = np.ogrid[bx[0]:bx[1]:bx[2]*1j, by[0]:by[1]:by[2]*1j, bz[0]:bz[1]:bz[2]*1j]
    # x, y, z = np.ogrid[-30:30:60j, -30:30:60j, -30:30:60j]
    # spacing: (max-min)/num (or num-1?)
    sx = (bx[1]-bx[0])/(bx[2]-1)
    sy = (by[1]-by[0])/(by[2]-1)
    sz = (bz[1]-bz[0])/(bz[2]-1)
    b = Box.from_data(distobj['box'])
    vb = VolBox(b, distobj['radius'])
    vb.data = distobj
    dm = vb.get_distance_numpy(x, y, z)
    verts, faces, norms, vals = marching_cubes_lewiner(dm, 0.0, spacing=(sx, sy, sz))
    mesh = get_compas_mesh(verts, faces)
    # return str(mesh.number_of_vertices())
    return str(mesh.to_data())
    # return mesh.to_json()
    # return verts, faces


def get_iso_vfs(distobj, bounds):
    from skimage.measure import marching_cubes_lewiner
    import numpy as np
    from compas_vol.primitives import VolBox
    from compas.geometry import Box

    bx = bounds[0]
    by = bounds[1]
    bz = bounds[2]
    x, y, z = np.ogrid[bx[0]:bx[1]:bx[2]*1j, by[0]:by[1]:by[2]*1j, bz[0]:bz[1]:bz[2]*1j]
    # x, y, z = np.ogrid[-30:30:60j, -30:30:60j, -30:30:60j]
    # spacing: (max-min)/num (or num-1?)
    sx = (bx[1]-bx[0])/(bx[2]-1)
    sy = (by[1]-by[0])/(by[2]-1)
    sz = (bz[1]-bz[0])/(bz[2]-1)
    b = Box.from_data(distobj['box'])
    vb = VolBox(b, distobj['radius'])
    vb.data = distobj
    dm = vb.get_distance_numpy(x, y, z)
    verts, faces, norms, vals = marching_cubes_lewiner(dm, 0.0, spacing=(sx, sy, sz))
    return (verts, faces)


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


def export_ipv_mesh(mesh, filename='ipv_mesh.obj', colors=None):
    """
    Exports a mesh of type :class:`ipyvolume.widgets.Mesh`
    to an .obj file at specified location.
    """

    import numpy as np

    vs = np.vstack((mesh.x, mesh.y, mesh.z)).T
    # vs = ['v {:.4f} {:.4f} {:.4f}'.format(v[0], v[1], v[2]) for v in vs]
    vs = ['v {} {} {}'.format(v[0], v[1], v[2]) for v in vs]
    if colors is not None:
        vs = [vs[i]+' {} {} {}'.format(c[0], c[1], c[2]) for i, c in enumerate(colors)]
    fs = ['f {} {} {}'.format(v[0]+1, v[1]+1, v[2]+1) for v in mesh.triangles]

    with open(filename, 'w') as f:
        f.write('\n'.join(vs))
        f.write('\n')
        f.write('\n'.join(fs))


def get_random_vector_2D():
    angle = random.random() * math.pi * 2
    vx = math.cos(angle)
    vy = math.sin(angle)
    return (vx, vy)


def get_random_vector_3D():
    angle = random.random() * math.pi * 2
    vz = random.random() * 2 - 1
    vx = math.sqrt(1 - vz**2) * math.cos(angle)
    vy = math.sqrt(1 - vz**2) * math.sin(angle)
    return (vx, vy, vz)


def get_compas_mesh(v, f):
    from compas.datastructures import Mesh
    m = Mesh.from_vertices_and_faces(v, f)
    return m


def draw_compas_mesh(mesh, color='white', size=1.0):
    """
    Renders a compas mesh on a 3D canvas with ipyvolume.

    Parameters
    ----------
    mesh : :class: compas.datastructures.Mesh
        the mesh to be shown in 3D

    Returns
    -------
    an instance of ipyvolume.widgets.Mesh
    """
    import ipyvolume as ipv

    # extract lists of vertices and faces
    vertices, faces = mesh.to_vertices_and_faces()

    # extract x, y and z values into separate lists
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    # triangulate n-gons
    triangles_only = []
    for f in faces:
        if len(f) == 3:
            triangles_only.append(f)
        else:
            for i in range(len(f) - 2):
                triangles_only.append([f[0], f[i+1], f[i+2]])

    # create the ipyvolume plot
    ipv.figure(width=800, height=450)
    viewermesh = ipv.plot_trisurf(x, y, z, triangles_only, color=color)
    ipv.xyzlim(size)
    ipv.style.use('minimal')
    ipv.show()

    return viewermesh


def export_layer(distfield, resolution, level, filename='layerimage.png'):
    """
    Exports a slice through a distance field as an image.
    """

    import numpy as np
    from skimage import io
    # add support for marching squares > outline

    # x, y = np.ogrid[-10:10:resolution+0j, -10:10:resolution+0j]
    y, x = np.ogrid[-10:10:resolution*1j, -10:10:resolution*1j]
    d = distfield.get_distance_numpy(x, y, level)

    # linear gradient
    # d = d - d.min()
    # m = d / d.max()

    # binary image
    # m = (d < 0)*1.0

    # absolute
    # d = np.abs(d)
    # m = d / d.max()

    # with aliasing
    m = 1-(np.tanh(d)+1)/2

    io.imsave(filename, m)
    return d

# to visualize bounds with meshplot
# example: p.add_lines(*add_cube(lbx,ubx,lby,uby,lbz,ubz))
def add_cube(a,b,c,d,e,f):
    v1 = [a,c,e]
    v2 = [b,c,e]
    v3 = [b,d,e]
    v4 = [a,d,e]
    v5 = [a,c,f]
    v6 = [b,c,f]
    v7 = [b,d,f]
    v8 = [a,d,f]
    vs = [v1,v2,v3,v4,v1,v2,v3,v4,v5,v6,v7,v8]
    ve = [v2,v3,v4,v1,v5,v6,v7,v8,v6,v7,v8,v5]
    #vs = np.array(vs)
    #ve = np.array(ve)
    return vs, ve

# if __name__ == "__main__":
#     from compas_vol.primitives import VolBox
#     from compas.geometry import Box, Frame

#     cb = Box(Frame((0, 0, 0), (1, 0.2, 0.1), (-0.1, 1, 0.2)), 16, 12, 8)
#     vb = VolBox(cb, 1.5)
#     o = export_layer(vb, 100, 0)
#     print(type(o))
