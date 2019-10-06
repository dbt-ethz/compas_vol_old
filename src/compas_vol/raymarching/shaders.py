import os
import re
from pathlib import Path

def get_shader_path(shader_name):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, shader_name)
    path = str(Path(path))
    path = re.sub(r':?\\', '/', path)
    path = str('/' + path)
    return path

print (get_shader_path('whatever.glsl'))   