import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import compas
from compas.datastructures import Mesh

sys.path.insert(0, "C:/Users/Ioanna/Documents/git_libraries/render_pipeline/") 
from rpcore import RenderPipeline

from rpcore import PointLight

# This is a helper class for better camera movement - see below.
from rpcore.util.movement_controller import MovementController


class PandaRendererPBR(ShowBase):
    def __init__(self):

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.pre_showbase_init()  

        ShowBase.__init__(self)
        
        self.render_pipeline.create(self)

        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr( Vec3(-17.2912578583, -13.290019989, 6.88211250305), Vec3(-39.7285499573, -14.6770210266, 0.0))
        self.controller.setup()

        ## group GeomNodes
        self.Meshes_group_node = GeomNode("MESHES")
        self.Lights_group_node = GeomNode("LIGHTS")
        self.Points_lines_group_node = GeomNode("POINTS_LINES")
        self.Text_group_node = GeomNode("TEXT")

        ## attach group nodes to 'render' nodePath
        self.nodePath_meshes_group = self.render.attachNewNode(self.Meshes_group_node)  
        self.nodePath_lights_group = self.render.attachNewNode(self.Lights_group_node)  
        self.nodePath_points_lines_group = self.render.attachNewNode(self.Points_lines_group_node)  
        self.nodePath_text_group = self.render.attachNewNode(self.Text_group_node) 

        self.create_lights()

        self.create_materials()

        self.render_pipeline.daytime_mgr.time = "12:20"

    def create_materials(self):
        self.metal = Material()
        self.metal.setDiffuse((1, 1, 1, 1))
        self.metal.setSpecular((0, 0, 0, 0))
        self.metal.setShininess(-1.804294705390930)
        self.metal.setAmbient((1, 1, 1, 1))
        self.metal.setAmbient((0, 0.615175, 0, 1))
        
        self.metal.setRoughness(1.7879559993743896)
        self.metal.setMetallic(0.6)
        self.metal.setRefractiveIndex(1.5)
        self.metal.setLocal(False)
    

    def create_lights(self):
        ## Default Lights
        my_light = PointLight()
        my_light.pos = (-1, -2, 10)
        my_light.color = (0.2, 0.6, 1.0)
        my_light.energy = 1000.0
        my_light.casts_shadows = True
        self.render_pipeline.add_light(my_light)

        ## Default Lights
        self.directional_light = DirectionalLight('directional_Light')
        self.directional_light_node_path = self.render.attachNewNode(self.directional_light)
        self.directional_light_node_path.reparentTo(self.nodePath_lights_group )

        self.ambient_light = AmbientLight('low_ambient_light')
        self.ambient_light.setColor(VBase4(0.5,0.5,0.5,1))
        self.ambient_light_node_path = self.render.attachNewNode(self.ambient_light)
        self.ambient_light_node_path.reparentTo(self.nodePath_lights_group )

        self.ambient_light2 = AmbientLight('strong_ambient_light')
        self.ambient_light2.setColor(VBase4(1,1,1,1))
        self.ambient_light_node_path2 = self.render.attachNewNode(self.ambient_light2)
        self.ambient_light_node_path2.reparentTo(self.nodePath_lights_group )

        ## assign lights to group nodes
        self.nodePath_meshes_group.setLight(self.ambient_light_node_path)
        self.nodePath_meshes_group.setLight(self.directional_light_node_path)
        self.nodePath_points_lines_group.setLight(self.ambient_light_node_path2)




    def print_scene_graph_b(self, node):
        for path in node.children.getPaths():
            print(path)
            self.print_scene_graph_b(path)

    def print_scene_graph(self):
        node = self.render
        for path in node.children.getPaths():
            print(path)
            self.print_scene_graph_b(path)


    def display_compas_mesh(self, mesh, name, normals = 'per face'):
        """
        Displays a compas mesh 

        Parameters
        ----------
        mesh   : (compas.datastructures.Mesh) compas Mesh
        name   : (string) Name of the shape on the scene graph.  
        normals: (string) If 'per face' : normals are displayed per face, then we see sharp corners. 
                          In any other case normlas are displayed per vertex, then we see smooth corners. 
        """
        assert isinstance(mesh, compas.datastructures.Mesh), "This is not a mesh, please change your input geometry"

        mesh_faces = [mesh.face[key] for key in list(mesh.faces())]
        mesh_vertices = [mesh.vertex_coordinates(key) for key in list(mesh.vertices())]   

        format = GeomVertexFormat.getV3n3c4t2() # vec3 vertex, vec3 normal, vec4 color, vec2 texcoord
        vdata = GeomVertexData('static_prim', format, Geom.UHStatic)
        vdata.setNumRows(3)

        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')
        normal_writer = GeomVertexWriter(vdata , 'normal')
        texture_writer = GeomVertexWriter(vdata , 'texcoord')

        geom = Geom(vdata)    

        ### Per face normals
        if normals == 'per face':    
            for face, fkey in zip(mesh_faces, list(mesh.faces())):
                face_normal = mesh.face_normal(fkey)

                for vertex_key in face:
                    vertex = mesh_vertices[vertex_key]
                    vertex_writer.addData3f(vertex[0] , vertex[1] , vertex[2])
                    normal_writer.addData3f(face_normal[0] , face_normal[1] , face_normal[2])
                    texture_writer.addData2f(0.0 , 0.0)
                    color_writer.addData4f(1., 1., 1., 1.)
                    # color_writer.addData4f((1+face_normal[0])/2 , (1+face_normal[1])/2 , (1+face_normal[2])/2, 1.)

                if len(face) > 3: 
                    print (len(face))
                    current_row_index = vdata.getNumRows() -1
                    c = current_row_index - (len(face)-1)
                    ## add more than one triangles
                    for i in range(len(face) -2):
                        triangle = GeomTriangles(Geom.UHStatic)
                        triangle.addVertices(c, c + 1 + i, c + 2 + i)
                        triangle.close_primitive()
                        geom.addPrimitive(triangle)
                else:   
                    current_row_index = vdata.getNumRows() -1
                    triangle = GeomTriangles(Geom.UHStatic)
                    triangle.addVertices(current_row_index, current_row_index - 1, current_row_index -2)
                    triangle.close_primitive()
                    geom.addPrimitive(triangle)

        ### Per vertex normals
        else: 
            mesh_vertex_normals = [mesh.vertex_normal(key) for key in list(mesh.vertices())]
            [vertex_writer.addData3f(v[0] , v[1] , v[2]) for v in mesh_vertices]
            [normal_writer.addData3f(n[0] , n[1] , n[2]) for n in mesh_vertex_normals]
            [color_writer.addData4f(1., 1., 1., 1.) for v in mesh_vertices]
            [texture_writer.addData2f(0.0 , 0.0) for v in mesh_vertices]
            # [color_writer.addData3f((n[0] + 1) /2, (n[1] + 1) /2 , (n[2] + 1) /2) for n in mesh_vertex_normals]

            for face in mesh_faces:
                if len(face) > 3:
                    for i in range(2): ## two triangles for one quad
                        triangle = GeomTriangles(Geom.UHStatic)
                        triangle.addVertices(face[0 + 2*i], face[1+ 2*i], face[(2+ 2*i)%4])
                        triangle.close_primitive()
                        geom.addPrimitive(triangle)
                else: 
                        triangle = GeomTriangles(Geom.UHStatic)
                        triangle.addVertices(face[0], face[1], face[2])
                        triangle.close_primitive()
                        geom.addPrimitive(triangle)

        # print (vdata)
        print ("number of primitives : ", geom.get_num_primitives())

        node = GeomNode(name)
        node.addGeom(geom)
        nodePath = NodePath(node)
        nodePath.setTwoSided(True)

        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_meshes_group)
        self.render_pipeline.prepare_scene(nodePath)
        nodePath.setMaterial(self.metal)

        # print ("nodePath.findAllVertexColumns()" )
        # print (nodePath.findAllVertexColumns())   



if __name__ == "__main__":
    pbr_renderer = PandaRendererPBR()
    pbr_renderer.run()