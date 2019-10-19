import numpy as np
from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus
from compas.datastructures import subdivision as sd

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer

## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', 'win-size 1024 760') 

def extrude(mesh, label_to_extrude, new_label, distance, delete_old_face = True):
    keys_of_faces_to_extrude = []
    for key, data in mesh.faces(True):
#         if data.get('label') == label_to_extrude:
        if mesh.get_face_attribute(key, 'ftype') == label_to_extrude:
            keys_of_faces_to_extrude.append(key)
    
    for key in keys_of_faces_to_extrude:
        print ('key: ', key)
        vertex_keys = mesh.face_vertices(key)
        new_vertex_keys = []
        new_face_keys = [] 
        normal = mesh.face_normal(key)
            
        ## create new vertices
        for i in range(len(vertex_keys)):  
            v = mesh.vertex[vertex_keys[i]] 
            new_vertex_key = mesh.add_vertex(x= v['x'] + normal[0] *distance, \
                                             y= v['y'] + normal[1] *distance, \
                                             z= v['z'] + normal[2] *distance)
            new_vertex_keys.append(new_vertex_key)
                
        ## create new side faces
        fourth_face_vertices = []
        for i in range(len(vertex_keys)):
            v          = vertex_keys[i]
            v_new      = new_vertex_keys[i]
            v_next     = vertex_keys[(i+1)% len(vertex_keys)] 
            v_next_new = new_vertex_keys[(i+1)% len(vertex_keys)]
                                
            new_face = [v, v_new, v_next_new , v_next]
            new_face_key = mesh.add_face(new_face)
            new_face_keys.append(new_face_key)
            mesh.set_face_attribute(new_face_key, 'ftype', new_label)
            
            fourth_face_vertices.append(v_new)
        
        ## create and label new fourth face
        new_face_key = mesh.add_face(fourth_face_vertices)
        new_face_keys.append(new_face_key)
        mesh.set_face_attribute(new_face_key, 'ftype', new_label)
        
        ## delete old face
    if delete_old_face:
        for key in keys_of_faces_to_extrude:
            mesh.delete_face(key)


def create_test_mesh_a():
    vertices = [[0.0, 0.0, 4.0], [1.0, 0.0, 4.0], [1.0, 1.0, 4.0], [0.0, 1.0, 4.0]]
    faces = [[0, 1, 2, 3]]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    mesh = sd.mesh_subdivide_tri(mesh, k=2)

    for index, (key, data) in enumerate(mesh.faces(True)):
        if index % 3 == 0:
            mesh.set_face_attribute(key, 'ftype', 'to_extrude')
        else: 
            mesh.set_face_attribute(key, 'ftype', 'start')

    ## move vertices up
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        if index > 4:
            attr['z'] += 0.2   
            
    extrude(mesh, 'to_extrude', 'extruded', 0.1)

    return mesh

def create_test_mesh_b():
    vertices = [
        [0.5, 0.0, 2.0],
        [0.0, 1.0, 2.0],
        [-0.5, 0.0, 2.0],
        [1.0, 1.0, 2.0]
    ]
    faces = [
        [0, 1, 2],
        [1, 0, 3]
    ]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    subd = sd.mesh_subdivide_tri(mesh)
    # subd = sd.trimesh_subdivide_loop(mesh, k=2)
    # subd = sd.mesh_subdivide_catmullclark(mesh)
    # subd = sd.mesh_subdivide_doosabin(subd)

    return subd

        



if __name__ == "__main__":

    renderer = PandaRenderer()

    ground_box = Box(Frame(Point(0., 0., 0.), [1., 0, 0], [0, 1., 0]), 3., 3., .5)  
    ground_box_mesh = Mesh.from_vertices_and_faces(ground_box.vertices, ground_box.faces) 

    renderer.display_compas_mesh( mesh = ground_box_mesh, name = 'ground_box')
    renderer.display_compas_mesh( mesh = create_test_mesh_a(), name = 'mesh_a', normals = 'per face')
    # renderer.display_compas_mesh( mesh = create_test_mesh_b(), name = 'mesh_b', normals = 'per face')

    renderer.display_axes_xyz(3)
    renderer.print_scene_graph()

    renderer.show()



