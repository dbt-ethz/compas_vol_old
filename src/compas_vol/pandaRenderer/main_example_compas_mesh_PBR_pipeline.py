import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus, Vector
from compas.datastructures import subdivision as sd

from compas_vol.pandaRenderer.pandaRendererPBR import PandaRendererPBR
from skimage.measure import marching_cubes_lewiner

from compas_vol.primitives import *

import shapes_temporary
import re

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', """ # win-size 1600 900 
                          window-title PandaRendererPBR example """) 


lb = 0   # lower boundary (for now keep to 0)
ub = 5  # upper boundary 

def discretize_distance_field_in_array(distance_field):
    num = 40 # resolution of grid
    fact = (ub-lb)/(num-1) #size of grid-cell

    x, y, z = np.ogrid[lb:ub:40j, lb:ub:40j, lb:ub:40j]
    m = distance_field.get_distance_numpy(x, y, z)
    return m, fact

def create_marching_cubes_mesh(distance_field):
    m, fact = discretize_distance_field_in_array(distance_field)
    verts, faces, normals, values = marching_cubes_lewiner(m, 0.0, spacing=(fact, fact, fact))
    return verts, faces, normals, values 

def get_material_info(mtl):
    info = "name: " + mtl.name + '\n' + "color: " +  ' , '.join(re.findall(r'\d+.\d+' , str(mtl.getBaseColor())))  + '\n' \
         + "metallic: " + str(mtl.getMetallic()) + '\n' \
         + "roughness: " + str(round (mtl.getRoughness(), 3)) + "\n" \
         + "emission: " +  ' , '.join(re.findall(r'\d+(?:.\d+)?' , str(mtl.getEmission())))
    return info



if __name__ == "__main__":

    rendererPBR = PandaRendererPBR()

    ground_box = Box(Frame(Point(-30., -30., 0.), [1., 0, 0], [0, 1., 0]), 60., 60., .5)  
    ground_box_mesh = Mesh.from_vertices_and_faces(ground_box.vertices, ground_box.faces) 
    gb_nodepath = rendererPBR.display_compas_mesh_PBR( mesh = ground_box_mesh, name = 'ground_box', normals = 'per face')
    

    for i in range(10):
        x = - 20 + 4 * i
        y = -6
        z = 1
        torus = shapes_temporary.Torus( Plane(Point(x,y,z), Vector(0,0,1)), 1, 0.5)
        verts, faces = torus.to_vertices_and_faces(u = 20, v = 20)
        torus_mesh = Mesh.from_vertices_and_faces(verts, faces)
        mtl = rendererPBR.materials_collection.find_material(str(i))
        rendererPBR.display_compas_mesh_PBR( mesh = torus_mesh, name = 'torus', normals = 'per vertex', material = mtl) 

        rendererPBR.display_text_3D(t = get_material_info(mtl) , dx=x-2 , dy=y + 1, dz=z+2, scale = 0.28)

    for i in range(11):
        x = - 20 + 4 * i
        y = 3
        z = 1.6
        sphere = shapes_temporary.Sphere(Point(x,y,z), 1)
        verts, faces = sphere.to_vertices_and_faces(u = 20, v = 20)
        mesh = Mesh.from_vertices_and_faces(verts, faces)
        mtl = rendererPBR.materials_collection.find_material(str(i + 10))
        rendererPBR.display_compas_mesh_PBR( mesh = mesh, name = 'sphere', normals = 'per vertex', material = mtl) 

        rendererPBR.display_text_3D(t = get_material_info(mtl) , dx=x-2 , dy=y + 1, dz=z+2, scale = 0.28)

    cylinder = shapes_temporary.Cylinder( Circle( Plane(Point(0,12,6), Vector(0,0,1)), 2),3)
    verts, faces = cylinder.to_vertices_and_faces(u = 20, v = 20)
    cylinder_mesh = Mesh.from_vertices_and_faces(verts, faces)
    cylinder_nodepath = rendererPBR.display_compas_mesh_PBR( mesh = cylinder_mesh, name = 'cylinder', normals = 'per face', uv_mapping = True) 

    rendererPBR.apply_texture(cylinder_nodepath, 0, 'materials/debugging_texture.png')
    # rendererPBR.apply_texture(cylinder_nodepath, 1, 'materials/MetalNormal.png')
    # rendererPBR.apply_texture(cylinder_nodepath, 3, 'materials/MetalSpecular.png')

    ### marching cubes mesh
    # torus = VolTorus(Torus(Plane((0, 0, 0), (0., 0., 1.)), 1.5, 0.6))
    # verts, faces, normals, values = create_marching_cubes_mesh(torus)
    # rendererPBR.create_mesh_from_marching_cubes_PBR(verts, faces, normals, 'marching_cubes_primitive',  material = rendererPBR.materials_collection.find_material('metal'))

    rendererPBR.run()








   










