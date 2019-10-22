import numpy as np
import sys, os

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer
from compas_vol.raymarching.rayMarchingFactory import RayMarchingFactory
from compas_vol.raymarching.translator import Translator

main_path = os.path.abspath(os.path.dirname(__file__))

from panda3d.core import loadPrcFileData    
loadPrcFileData('', ' win-size 1024 1024') 

if __name__ == "__main__":
    renderer = PandaRenderer()

    translator = Translator(None)

    rayMarcher = RayMarchingFactory( main_path , renderer, translator)
    rayMarcher.ray_marching_shader( default_fragment_shader = False, custom_fragment_shader = "fshader_custom.glsl")
    # rayMarcher.post_processing_ray_marching_filter( default_fragment_shader = False, custom_fragment_shader = "fshader_deconstruction_tutorial.glsl")

    renderer.show()