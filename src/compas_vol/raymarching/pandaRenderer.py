import os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomVertexArrayFormat,LVector3,LVector2f, MeshDrawer, LVector3f, LVector4, PerspectiveLens, Texture, TransparencyAttrib, OccluderNode ,OmniBoundingVolume,  SceneSetup, Shader, LPoint3, LMatrix4, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, GeomLines, GeomPoints, DirectionalLight, AmbientLight, VBase4, Material, TextNode
from direct.gui.OnscreenText import OnscreenText

from direct.filter.FilterManager import FilterManager
from direct.filter.CommonFilters import CommonFilters

import numpy as np
from compas_vol.raymarching.remapping_functions import map_values_to_colors

from direct.filter.CommonFilters import CommonFilters

from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectGui import *

from direct.task import Task


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
        self.setFrameRateMeter(True)
        # self.cam.setPos(8,-40,5)   

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

        ## Default Lights
        self.directional_light = DirectionalLight('directional_Light')
        self.directional_light_node_path = self.render.attachNewNode(self.directional_light)
        self.directional_light_node_path.reparentTo(self.nodePath_lights_group )

        self.ambient_light = AmbientLight('low_ambient_light')
        self.ambient_light.setColor(VBase4(0.2,0.2,0.2,1))
        self.ambient_light_node_path = self.render.attachNewNode(self.ambient_light)
        self.ambient_light_node_path.reparentTo(self.nodePath_lights_group )

        self.ambient_light2 = AmbientLight('strong_ambient_light')
        self.ambient_light2.setColor(VBase4(1,1,1,1))
        self.ambient_light_node_path2 = self.render.attachNewNode(self.ambient_light2)
        self.ambient_light_node_path2.reparentTo(self.nodePath_lights_group )

        ## assign lights to group nodes
        self.nodePath_meshes_group.setLight(self.directional_light_node_path)
        self.nodePath_meshes_group.setLight(self.ambient_light_node_path)
        self.nodePath_points_lines_group.setLight(self.ambient_light_node_path2)

        self.display_axes_xyz(3)

    def print_scene_graph_b(self, node):
        for path in node.children.getPaths():
            print(path)
            self.print_scene_graph_b(path)

    def print_scene_graph(self):
        node = self.render
        for path in node.children.getPaths():
            print(path)
            self.print_scene_graph_b(path)

    def create_compas_primitive(self, primitive, name):
        """
        WIP. Didn't have time to finish this yet
        """

        format = GeomVertexFormat.getV3n3c4() # vec3 vertex, vec3 normal, vec4 color
        vdata = GeomVertexData('static_prim', format, Geom.UHStatic)
        vdata.setNumRows(len(primitive.vertices))

        vertex_writer = GeomVertexWriter(vdata , 'vertex')
        # color_writer  = GeomVertexWriter(vdata , 'color')
        # normal_writer = GeomVertexWriter(vdata , 'normal')

        [vertex_writer.addData3f(v[0] , v[1] , v[2]) for v in primitive.vertices ]

        geom = Geom(vdata)

        for face in primitive.faces:
            if len(face) > 3:
                for i in range(2):
                    triangle = GeomTriangles(Geom.UHStatic)
                    triangle.addVertices(face[0 + 2*i], face[1+ 2*i], face[(2+ 2*i)%4])
                    triangle.close_primitive()
                    geom.addPrimitive(triangle)
            else: 
                    triangle = GeomTriangles(Geom.UHStatic)
                    triangle.addVertices(face[0], face[1], face[2])
                    triangle.close_primitive()
                    geom.addPrimitive(triangle)

        node = GeomNode(name)
        node.addGeom(geom)
        nodePath = NodePath(node)
        nodePath.setTwoSided(True)
        nodePath.setScale(1,1,1)

        nodePath = self.render.attachNewNode(node)  
        nodePath.reparentTo(self.nodePath_meshes_group)
        # nodePath.setMaterial(mtl)

    def create_mesh_from_marching_cubes(self, vertices, faces, normals, name):  #
        """
        Creates and displays a panda3d shape from a marching cubes algorithm 

        Parameters
        ----------
        vertices: (array) Vertices of mesh
        faces   : (array) Faces of mesh
        normals : (array) Normals of mesh. Attention normals are inverted because using the marching_cubes_lewiner from skimage.measure they came in inverted
        name    : (string) Name of the shape on the scene graph.  
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
        # nodePath.setMaterial(mtl)

    def create_boundary_box(self, n):
        """ Displays a wireframe box 
        
        Parameters
        ----------
        n: (float) Upper boundary of the box. Lower boundary has to be 0 (SHOULD FIX THIS)
        """

        format = GeomVertexFormat.getV3() # vec3 vertex
        vdata = GeomVertexData('bounding_box', format, Geom.UHStatic)
        vdata.setNumRows(8) # 8 points in total
        vertex_writer = GeomVertexWriter(vdata , 'vertex')

        #write vertices
        corners = [[0,0,0] , [n,0,0] , [n,n,0] , [0,n,0] , [0,0,n] , [n,0,n] , [n,n,n] , [0,n,n] ] 
        for c in corners: 
            vertex_writer.addData3f(c[0] , c[1] , c[2])

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
                    self.create_text(str(value), x, y, z, fact * 0.25)
        

    def create_text(self, t, dx, dy, dz, scale = 0.08):
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
        textNode.setText(t)
        textNode.setTransform(Translation_matrix(dx/scale, dy/scale, dz/scale))
        textNodePath = self.render.attachNewNode(textNode)
        textNodePath.setScale(scale)
        textNodePath.reparentTo(self.nodePath_text_group)

    def create_onscreen_text(self, t, pos_x, pos_y, s):
        textObject = OnscreenText(text = t, pos = (pos_x, pos_y), scale = s)
        






    def show(self):     
        """
        Starts the renderer viewport.
        Attention, it should be the last function you call, anything that comes after it will not run untill the window exits.
        """
        
        self.run()



def Translation_matrix(dx, dy, dz):
    return LMatrix4(1,0,0,0 , 0,1,0,0 , 0,0,1,0 , dx,dy,dz,1)


if __name__ == "__main__":
## Default ShowBase
    renderer = PandaRenderer()
    renderer.display_axes(4)
    # renderer.create_onscreen_text("Title", -0.5,-0.5,0.05)
    # renderer.print_scene_graph()
    renderer.create_slicing_slider()
    renderer.show()
