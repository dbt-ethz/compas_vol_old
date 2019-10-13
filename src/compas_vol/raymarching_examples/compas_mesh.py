import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus

from compas_vol.raymarching.pandaRenderer import PandaRenderer

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', 'win-size 1024 760') 

if __name__ == "__main__":
    ## Create compas primitive



    ### panda3d visualisation
    renderer = PandaRenderer()

    ##############
    ## NEED TO CALCULATE NORMALS PER FACE
    ##############
    ground_box = Box(Frame(Point(0., 0., 0.), [1., 0, 0], [0, 1., 0]), 3., 3., .5)   

    faces = ground_box.faces
    vertices = ground_box.vertices
    ground_box_mesh = Mesh.from_vertices_and_faces(vertices, faces) 
    # print (mesh.summary())

    renderer.display_compas_mesh(ground_box_mesh, 'ground_box')
    renderer.show()




   










