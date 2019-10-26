import numpy as np
import sys, os
import random

import compas_vol
from compas_vol.primitives import *
from compas_vol.combinations import *
from compas_vol.modifications import *
from compas_vol.microstructures import *

from skimage.measure import marching_cubes_lewiner

from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer
from compas_vol.raymarching.rayMarchingFactory import RayMarchingFactory
from compas_vol.raymarching.translator import Translator

from compas_vol.raymarching.remapping_functions import remap


## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', """ # win-size 1024 700
                          window-title Raymarching example 
                          sync-video 0 """) 

main_path = os.path.abspath(os.path.dirname(__file__))

sqrt2 = 1.41421

if __name__ == "__main__":
    ## --------------------------- Geometry

    ## box
    box_dim_w = 3.5
    box_dim_h = 12.
    box = VolBox(Box(Frame(Point(0., 0., 0.), [1, 0, 0], [0, 1., 0]), box_dim_w, box_dim_w, box_dim_h), 0.1)
    b = box_dim_w/2
    box_corners = [[b , -b], [-b, -b], [-b, b], [b, b]]

    spheres_list = []

    height_num = 4
    for i in range(height_num): #height
        for corner in box_corners: # corner
            height = i * box_dim_h/(height_num-1) - box_dim_h/2
            sphere = VolSphere(Sphere(Point(corner[0], corner[1], height), 1. + i* 0.25))
            spheres_list.append(sphere)
    spheres = Union(spheres_list)

    total_geom = Subtraction(box, spheres)

    ## --------------------------- Visualization
    renderer = PandaRenderer()
    # renderer.display_axes_xyz(3)  

    translator = Translator(total_geom)
    rayMarcher = RayMarchingFactory(main_path, renderer, translator, bounding_sphere = [box_dim_w/2, box_dim_w/2, box_dim_h/2, 15.])
    rayMarcher.post_processing_ray_marching_filter()
    # rayMarcher.ray_marching_shader()
    rayMarcher.show_csg_tree_GUI()
    rayMarcher.create_slicing_slider(-7, 16 ,-7)

    renderer.show()
