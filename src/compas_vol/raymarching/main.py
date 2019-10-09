import numpy as np

import compas_vol
from compas_vol.primitives import *
from compas_vol.combinations import *
from compas_vol.modifications import *

from skimage.measure import marching_cubes_lewiner

from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus


from compas_vol.raymarching.pandaRenderer import PandaRenderer
from compas_vol.raymarching.rayMarchingFactory import RayMarchingFactory
from compas_vol.raymarching.translator import Translator

from compas_vol.raymarching.remapping_functions import remap

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', 'win-size 1024 760') 

num = 30 # resolution of grid
lb = 0   # lower boundary (for now keep to 0)
ub = 10  # upper boundary 
fact = (ub-lb)/(num-1) #size of grid-cell


def rand(lb_, ub_):
    value = np.random.rand(1)
    return remap(value, 0, 1, lb_, ub_)


def discretize_distance_field_in_array(distance_field):
    x, y, z = np.ogrid[lb:ub:30j, lb:ub:30j, lb:ub:30j]
    m = distance_field.get_distance_numpy(x, y, z)
    return m



if __name__ == "__main__":
    ## Create compas_vol primitives
    Spheres = []
    for i in range(10):
        mySphere = VolSphere(Sphere(Point(rand(lb+1,ub-1), rand(lb+1,ub-1), rand(lb+1,ub-1)), rand(2.,3.)))
        Spheres.append(mySphere)
    union_spheres = Union(Spheres)

    ## test compas_vol shapes
    torus = VolTorus(Torus(Plane((3, 3, 3), (1., 0., 1.)), 2.0, 1.0))
    sphere =  VolSphere(Sphere(Point(2, 2, 2), 2))
    cylinder = VolCylinder(Cylinder(Circle(Plane([2, 3, 4], [0.3, 0.4, 1.]), 2.0), 3.0))
    box = VolBox(Box(Frame(Point(3., 3., 3.), [3., 3.5, 0.1], [2.5, 1., 2.1]), 10, 11, 12), 1)
    union = Union(VolSphere(Sphere(Point(5, 6, 3), 3)), VolSphere(Sphere(Point(1, 2, 3), 2)))
    intersection = Intersection(VolSphere(Sphere(Point(5, 6, 3), 3)), VolSphere(Sphere(Point(1, 2, 3), 9)))
    sh = SmoothUnion(Shell(union, 0.3, 0.5) , Shell(union_spheres, 0.1, 0.5), 2.) 

    total_geom =  SmoothUnion(Shell(Union(sphere, torus), 0.3, 0.5), Shell(union_spheres, 0.3, 0.5), 2.) #Intersection(sphere, box)  #Union(Union(torus , sphere), Union(intersection, cylinder))
    

    ### panda3d visualisation
    renderer = PandaRenderer()

    # m = discretize_distance_field_in_array(total_geom)
    # verts, faces, normals, values = marching_cubes_lewiner(m, 0.0, spacing=(fact, fact, fact))
    # renderer.create_mesh_from_marching_cubes(verts, faces, normals, 'marching_cubes_primitive')

    # renderer.create_boundary_box(ub) #lb has to be 0 for now
    # renderer.print_scene_graph()§
    # renderer.display_volumetric_grid(lb, ub, m, num, fact, True)

    translator = Translator(total_geom)

    rayMarcher = RayMarchingFactory(renderer, translator)
    rayMarcher.post_processing_ray_marching_filter()
    # rayMarcher.ray_marching_shader()
    rayMarcher.show_csg_tree_GUI()
    rayMarcher.create_slicing_slider(-7, 16 ,-7)
    # # rayMarcher.create_general_purpose_slider()

    ### WIP
    # ground_box = Box(Frame(Point(0., 0., 0.), [1., 0, 0], [0, 1., 0]), 3., 3., .5)    
    # renderer.create_compas_primitive(ground_box, 'ground_box')

    renderer.show()



   










