"""
********************************************************************************
primitives
********************************************************************************
.. currentmodule:: compas_vol.primitives
Classes
=======
Subheading
----------
.. autosummary::
    :toctree: generated/
    :nosignatures:
    VolBox
    VolSphere
    VolCylinder
    VolTorus
    VolCapsule
    VolCone
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .gdf import *
from .heart import *
from .vbox import *
from .vcapsule import *
from .vcone import *
from .vcylinder import *
from .vplane import *
from .vpolyhedron import *
from .vsphere import *
from .vtorus import *

__all__ = [name for name in dir() if not name.startswith('_')]
