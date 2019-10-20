import sys
from direct.showbase.ShowBase import ShowBase

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer
from panda3d.core import *
import compas
from compas.datastructures import Mesh

sys.path.insert(0, "C:/Users/Ioanna/Documents/git_libraries/render_pipeline/") 
from rpcore import RenderPipeline

from rpcore import PointLight

# This is a helper class for better camera movement - see below.
from rpcore.util.movement_controller import MovementController


class PandaRendererPBR(PandaRenderer):
    def __init__(self):

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.pre_showbase_init()  
        
        PandaRenderer.__init__(self)

        self.render_pipeline.create(self)
        self.render_pipeline.daytime_mgr.time = "12:20"

        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr( Vec3(-17.2912578583, -13.290019989, 6.88211250305), Vec3(-39.7285499573, -14.6770210266, 0.0))
        self.controller.setup()

        self.create_materials()


    def create_materials(self):
        self.metal = Material()
        self.metal.setDiffuse((1, 1, 1, 1))
        self.metal.setSpecular((0, 0, 0, 0))
        self.metal.setShininess(-1.804294705390930)
        self.metal.setAmbient((1, 1, 1, 1))
        self.metal.setAmbient((0, 0.615175, 0, 1))
        
        self.metal.setRoughness(1.7879559993743896)
        self.metal.setMetallic(0.0)
        self.metal.setRefractiveIndex(1.5)
        self.metal.setLocal(False)
    

    def create_lights_PBR(self):
        ## Default Lights
        my_light = PointLight()
        my_light.pos = (-1, -2, 10)
        my_light.color = (0.2, 0.6, 1.0)
        my_light.energy = 1000.0
        my_light.casts_shadows = True
        self.render_pipeline.add_light(my_light)




    def display_compas_mesh_PBR(self, mesh, name, normals = 'per face'):
        """
        TO DO
        """
        nodePath = self.display_compas_mesh(mesh, name, normals = normals)
        self.render_pipeline.prepare_scene(nodePath)
        nodePath.setMaterial(self.metal)
        # print (nodePath.findAllVertexColumns())   
        return nodePath

    def create_mesh_from_marching_cubes_PBR(self, vertices, faces, normals, name):
        """
        TO DO
        """
        nodePath = self.create_mesh_from_marching_cubes(vertices, faces, normals, name)
        self.render_pipeline.prepare_scene(nodePath)
        nodePath.setMaterial(self.metal)
        return nodePath


if __name__ == "__main__":
    pbr_renderer = PandaRendererPBR()
    pbr_renderer.run()