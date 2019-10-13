import sys, os
from panda3d.core import Filename

def get_shader_path(main_path , shader_name):
    dir_path =  os.path.abspath(os.path.dirname(__file__))
    rel_path = os.path.relpath(dir_path, main_path)
    rel_path_unix_style = Filename.fromOsSpecific(rel_path).getFullpath()
    path = str(rel_path_unix_style + "/" + shader_name)
    return path