import os
from direct.showbase.ShowBase import ShowBase
# from direct.showbase import Loader
from panda3d.core import Geom, GeomVertexArrayFormat,LVector3,LVector2f, MeshDrawer, LVector3f, LVector4, PerspectiveLens, Texture, TransparencyAttrib, OccluderNode ,OmniBoundingVolume,  SceneSetup, Shader, LPoint3, LMatrix4, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, GeomLines, GeomPoints, DirectionalLight, AmbientLight, VBase4, Material, TextNode
from direct.gui.OnscreenText import OnscreenText

from direct.filter.FilterManager import FilterManager
from direct.filter.CommonFilters import CommonFilters

import numpy as np
import math
from compas_vol.raymarching.remapping_functions import map_values_to_colors

import compas
from direct.filter.CommonFilters import CommonFilters

from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectGui import *

from direct.task import Task

text_color_alpha = 0.5

class PandaRenderer(ShowBase):
    """
    Inherits from Panda3d Showbase, the built-in renderer class.
    Documentation: https://www.panda3d.org/reference/python/classdirect_1_1showbase_1_1ShowBase_1_1ShowBase.html
    Only one can exist in the scene.

    Creates the basic categories-nodepaths of the scene graph where the other nodepaths should be reparented.
    Creates default lights.

    """

    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(1,1,1)
        self.setFrameRateMeter(True)
        # self.cam.setPos(8,-40,5)   
        self.filters = CommonFilters(self.win, self.cam)

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

        # self.display_axes_xyz(3)
        self.create_lights()


    def create_lights(self):
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

    def display_compas_mesh(self, mesh, name, normals = 'per face', uv_mapping = True):
        """
        Displays a compas mesh 

        Parameters
        ----------
        mesh      : (compas.datastructures.Mesh) compas Mesh
        name      : (string) Name of the shape on the scene graph.  
        normals   : (string) If 'per face' : normals are displayed per face, then we see sharp corners. 
                             In any other case normlas are displayed per vertex, then we see smooth corners. 
        uv_mapping: (boolean) Apply uv_mapping on the mesh. Currently only cylindrical uv mapping along the z axis (zylindrical projection)

        Returns
        -------
        TO DO
        """
        assert isinstance(mesh, compas.datastructures.Mesh), "This is not a mesh, please change your input geometry"

        mesh_faces = [mesh.face[key] for key in list(mesh.faces())]
        mesh_vertices = [mesh.vertex_coordinates(key) for key in list(mesh.vertices())]   
        uvs = np.zeros(len(mesh_vertices))

        if uv_mapping:
            uvs = zylindrical_uv_mapping(mesh_vertices)

        format = GeomVertexFormat.getV3n3c4t2()	# vec3 vertex, vec3 normal, vec4 color, vec2 uv
        vdata = GeomVertexData('static_prim', format, Geom.UHStatic)
        vdata.setNumRows(3)

        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')
        normal_writer = GeomVertexWriter(vdata , 'normal')
        texcoord_writer = GeomVertexWriter(vdata , 'texcoord')
        geom = Geom(vdata)    

        ### Per face normals
        if normals == 'per face':    
            for face, fkey in zip(mesh_faces, list(mesh.faces())):
                face_normal = mesh.face_normal(fkey)

                for vertex_key in face:
                    vertex = mesh_vertices[vertex_key]
                    vertex_writer.addData3f(vertex[0] , vertex[1] , vertex[2])
                    normal_writer.addData3f(face_normal[0] , face_normal[1] , face_normal[2])
                    # color_writer.addData4f(1., 1., 1., 1.)
                    color_writer.addData4f((1+face_normal[0])/2 , (1+face_normal[1])/2 , (1+face_normal[2])/2, 1.)
                    texcoord_writer.addData2f(uvs[vertex_key][0] , uvs[vertex_key][1])

                if len(face) > 3: 
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
            [color_writer.addData3f(1., 1., 1. ) for _ in mesh_vertex_normals]
            # [color_writer.addData3f((n[0] + 1) /2, (n[1] + 1) /2 , (n[2] + 1) /2) for n in mesh_vertex_normals]  ## color according to normals
            [texcoord_writer.addData2f(uv[0] , uv[1]) for uv in uvs]

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
        # print ("number of primitives : ", geom.get_num_primitives())

        node = GeomNode(name)
        node.addGeom(geom)
        nodePath = NodePath(node)
        nodePath.setTwoSided(True)

        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_meshes_group)

        return nodePath
        # self.filters.setCartoonInk()

    def create_mesh_from_marching_cubes(self, vertices, faces, normals, name):  #
        """
        Creates and displays a panda3d shape from a marching cubes algorithm 

        Parameters
        ----------
        vertices: (array) Vertices of mesh
        faces   : (array) Faces of mesh
        normals : (array) Normals of mesh. Attention normals are inverted because using the marching_cubes_lewiner from skimage.measure they came in inverted
        name    : (string) Name of the shape on the scene graph.  

        Returns
        -------
        To Do
        """

        ## GeomVertexFormat
        format = GeomVertexFormat.getV3n3c4() # vec3 vertex, vec3 normal, vec4 color

        ## GeomVertexData
        vdata = GeomVertexData('static_prim', format, Geom.UHStatic)
        vdata.setNumRows(len(vertices))

        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')
        normal_writer = GeomVertexWriter(vdata , 'normal')

        #write vertices
        for i,v in enumerate(vertices): 
            vertex_writer.addData3f(v[0] , v[1] , v[2] )
            n = normals[i]
            normal_writer.addData3f(-n[0] , -n[1] , -n[2])
            color_writer.addData4f((n[0]+1)/2 , (n[1]+1)/2 , (n[2]+1)/2 , 1)

        ## Geom object 
        geom = Geom(vdata)

        #create primitives 
        for f in faces:
            triangle = GeomTriangles(Geom.UHStatic)
            triangle.addVertices(f[0],f[1],f[2])
            triangle.close_primitive()
            geom.addPrimitive(triangle)

        node = GeomNode(name)
        node.addGeom(geom)
        nodePath = NodePath(node)
        nodePath.setTwoSided(True)
        nodePath.setScale(1,1,1)

        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_meshes_group)
        return nodePath

    def display_boundary_box(self, ub):
        """ Displays a wireframe box 
        
        Parameters
        ----------
        ub: (float) Upper boundary of the box. Lower boundary has to be 0 (SHOULD FIX THIS)
        """

        format = GeomVertexFormat.getV3c4() # vec3 vertex, vec4 color 
        vdata = GeomVertexData('bounding_box', format, Geom.UHStatic)
        vdata.setNumRows(8) # 8 points in total
        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')

        #write vertices
        corners = [[0,0,0] , [ub,0,0] , [ub,ub,0] , [0,ub,0] , [0,0,ub] , [ub,0,ub] , [ub,ub,ub] , [0,ub,ub] ] 
        for c in corners: 
            vertex_writer.addData3f(c[0] , c[1] , c[2])
            color_writer.addData4f(0.,0.,0., text_color_alpha)

        #create primitives 
        geom = Geom(vdata)
        pairs = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
        for p in pairs:
            line = GeomLines(Geom.UHStatic)
            line.addVertices(p[0],p[1])
            line.close_primitive()
            geom.addPrimitive(line)

        node = GeomNode('boundary_box')
        node.addGeom(geom)
        nodePath = NodePath(node)
        # nodePath.setRenderModeThickness(1)
        nodePath.setTwoSided(True)
        nodePath.setScale(1,1,1)

        nodePath = self.render.attachNewNode(node)  
        nodePath.setLight(self.ambient_light_node_path2)

    def display_axes_xyz(self, size):
        """
        Displays the xyz axis with the usual color convention (x red, y gree, z blue).
        
        Parameters
        ----------
        size: (float) Length of axis.
        """

        format = GeomVertexFormat.getV3c4() # vec3 vertex, vec4 color
        vdata = GeomVertexData('axes', format, Geom.UHStatic)
        vdata.setNumRows(6) # 6 vertices in total
        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')

        #write vertices
        vertices = [[0,0,0] , [size,0,0] , [0,0,0] , [0,size,0] , [0,0,0] , [0,0,size]] 
        colors = [[1,0,0] , [1,0,0] , [0,1,0] , [0,1,0] , [0,0,1] , [0,0,1]] 
        for i,v in enumerate(vertices): 
            vertex_writer.addData3f(v[0] , v[1] , v[2])
            c = colors[i]
            color_writer.addData4f(c[0] , c[1] , c[2] , 1)

        #create primitives 
        geom = Geom(vdata)
        pairs = [[0,1],[2,3],[4,5]]
        for i,p in enumerate(pairs):
            line = GeomLines(Geom.UHStatic)
            line.addVertices(p[0],p[1])
            line.close_primitive()
            geom.addPrimitive(line)

        ## Node in graph 
        node = GeomNode('xyz_axes')
        node.addGeom(geom)

        #Nodepath
        nodePath = NodePath(node)
        nodePath.setRenderModeThickness(4)
        nodePath.setTwoSided(True)
        nodePath.setScale(1,1,1)
        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_points_lines_group) 

    def display_volumetric_grid(self, lb, ub, m, num, fact, showValues):
        """ Displays a grid of points that is colored depending on the values of the distance field
        
        Parameters
        ----------
        lb        : (float) lower boundary. For now keep to 0
        ub        : (float) upper boudnary
        m         : (numpy array) distance values
        num       : (int) resolution of grid
        fact      : (float) size of grid cell
        showValues: (bool) Toggle on/off the number text on the viewport. (Attention, has a considerable impact on performance)
        """

        format = GeomVertexFormat.getV3c4() # vec3 vertex, vec4 color

        ## GeomVertexData
        vdata = GeomVertexData('my_data', format, Geom.UHStatic)
        vdata.setNumRows(len(m))
        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        color_writer  = GeomVertexWriter(vdata , 'color')

        r,g,b = map_values_to_colors(m, num)

        #write vertices
        for i in range(num):
            for j in range(num):
                for k in range(num):
                    x = lb + k*fact
                    y = lb + j*fact
                    z = lb + i*fact
                    vertex_writer.addData3f(x , y , z)
                    color_writer.addData4f(r[k][j][i] , g[k][j][i] , b[k][j][i] , 1)

        #create primitives 
        geom = Geom(vdata)
        for i in range(num*num*num):
            point = GeomPoints(Geom.UHStatic)
            point.addVertex(i)
            point.closePrimitive()
            geom.addPrimitive(point)

        ## Node in graph 
        node = GeomNode('gnode')
        node.addGeom(geom)

        #Nodepath
        nodePath = NodePath(node)
        nodePath.setTwoSided(True)
        nodePath.setRenderModeThickness(10)
        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_points_lines_group)
        
        if showValues:
            self.display_volumetric_grid_values(lb, ub, m, num, fact)

    def display_volumetric_grid_values(self, lb, ub, m, num, fact):
        """
        Displays distance values of volumetric grid.
        Don't call independently, it's called by the 'display_volumetric_grid'
        """

        for i in range(num):
            for j in range(num):
                for k in range(num):
                    x = lb + k*fact
                    y = lb + j*fact
                    z = lb + i*fact
                    value = m[k][j][i]
                    value = round(value, 2)
                    self.display_text_3D(str(value), x, y, z, fact * 0.25)
 
    def display_text_3D(self, t, dx, dy, dz, scale = 0.08):
        """
        Creates and displays text.

        Parameters
        ----------
        t    : (string) Text to be displayed
        dx   : (float) Position x
        dy   : (float) Position y
        dz   : (float) Position z
        scale: (float) Scale of text
        """
    
        textNode = TextNode('text_name')
        textNode.setTextColor(0., 0., 0., text_color_alpha)
        textNode.setText(t)
        textNode.setTransform(Translation_matrix(dx/scale, dy/scale, dz/scale))
        textNodePath = self.render.attachNewNode(textNode)
        textNodePath.setScale(scale)
        textNodePath.reparentTo(self.nodePath_text_group)

    def display_onscreen_text(self, t, pos_x, pos_y, s):
        textObject = OnscreenText(text = t, pos = (pos_x, pos_y), scale = s, fg = (0., 0., 0., text_color_alpha) )

    def apply_texture(self, nodePath, path_to_texture):
        """
        TO DO
        """        
        ## test texture
        texture = self.loader.loadTexture(path_to_texture)
        nodePath.setTexture(texture, 1)

    def show(self):     
        """
        Starts the renderer viewport.
        Attention, it should be the last function you call, anything that comes after it will not run untill the window exits.
        """
        
        self.run()

def zylindrical_uv_mapping(mesh_vertices):
        us = np.zeros(len(mesh_vertices))
        vs = np.zeros(len(mesh_vertices))
        x_list = [v[0] for v in mesh_vertices]
        y_list = [v[1] for v in mesh_vertices]
        z_list = [v[2] for v in mesh_vertices]

        bounds = max(z_list) - min(z_list)
        if bounds == 0:
            bounds = 1

        for i, x, y, z in zip(range(len(mesh_vertices)), x_list, y_list, z_list):
            a = math.atan2(y, -x)/math.pi
            v = (z-min(z_list))/ bounds
            us[i] = (a+1)/2
            vs[i] = v

        return np.stack((us, vs),axis = 1 )

def Translation_matrix(dx, dy, dz):
    return LMatrix4(1,0,0,0 , 0,1,0,0 , 0,0,1,0 , dx,dy,dz,1)


if __name__ == "__main__":
## Default ShowBase
    renderer = PandaRenderer()
    renderer.display_axes(4)
    # renderer.display_onscreen_text("Title", -0.5,-0.5,0.05)
    # renderer.print_scene_graph()
    renderer.create_slicing_slider()
    renderer.show()
