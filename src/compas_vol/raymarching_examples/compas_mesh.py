import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus

from compas_vol.raymarching.pandaRenderer import PandaRenderer

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', 'win-size 1024 760') 

if __name__ == "__main__":

    renderer = PandaRenderer()

    ground_box = Box(Frame(Point(0., 0., 0.), [1., 0, 0], [0, 1., 0]), 3., 3., .5)   

    ground_box_mesh = Mesh.from_vertices_and_faces(ground_box.vertices, ground_box.faces) 
    print (ground_box_mesh.summary())

    renderer.display_compas_mesh( mesh = ground_box_mesh, name = 'ground_box', normals = 'per face')

    renderer.display_axes_xyz(3)
    renderer.show()




   










