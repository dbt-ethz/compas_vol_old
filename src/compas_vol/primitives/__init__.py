"""
********************************************************************************
compas_vol.primitives
********************************************************************************

.. currentmodule:: compas_vol.primitives

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    VolBox
    VolSphere
    VolCylinder
    VolTorus
    VolCapsule
    VolCone
    VolPlane
    VolExtrusion
    VolPolyhedron
    VolEllipsoid

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
from .vellipsoid import *
from .vextrusion import *
from .vplane import *
from .vpolyhedron import *
from .vsphere import *
from .vtorus import *

__all__ = [name for name in dir() if not name.startswith('_')]
