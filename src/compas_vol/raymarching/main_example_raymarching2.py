import numpy as np
import sys, os
import random

import compas_vol
from compas_vol.primitives import *
from compas_vol.combinations import *
from compas_vol.modifications import *
from compas_vol.microstructures import *

from skimage.measure import marching_cubes_lewiner

from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer
from compas_vol.raymarching.rayMarchingFactory import RayMarchingFactory
from compas_vol.raymarching.translator import Translator

from compas_vol.raymarching.remapping_functions import remap


## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', """ # win-size 1024 700
                          window-title Raymarching example 
                          sync-video 0 """) 

main_path = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    ## Create compas_vol primitives