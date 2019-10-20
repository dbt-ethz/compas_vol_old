import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus
from compas.datastructures import subdivision as sd

from compas_vol.pandaRenderer.pandaRendererPBR import PandaRendererPBR
from compas_vol.pandaRenderer.main_example_compas_mesh import extrude, create_test_mesh_a, create_test_mesh_b
from compas_vol.pandaRenderer.main_example_marching_cubes_mesh import discretize_distance_field_in_array, create_marching_cubes_mesh

from compas_vol.primitives import *

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', 'win-size 1024 760') 




if __name__ == "__main__":

    rendererPBR = PandaRendererPBR()

    ground_box = Box(Frame(Point(0., 0., 0.), [1., 0, 0], [0, 1., 0]), 3., 3., .5)  
    ground_box_mesh = Mesh.from_vertices_and_faces(ground_box.vertices, ground_box.faces) 

    rendererPBR.display_compas_mesh_PBR( mesh = ground_box_mesh, name = 'ground_box', normals = 'per face')
    rendererPBR.display_compas_mesh_PBR( mesh = create_test_mesh_a(), name = 'mesh_a', normals = 'per face')

    # rendererPBR.print_scene_graph()

    ### marching cubes mesh
    torus = VolTorus(Torus(Plane((3, 3, 3), (1., 0., 1.)), 2.0, 1.0))
    verts, faces, normals, values = create_marching_cubes_mesh(torus)
    rendererPBR.create_mesh_from_marching_cubes_PBR(verts, faces, normals, 'marching_cubes_primitive')

    rendererPBR.run()








   










