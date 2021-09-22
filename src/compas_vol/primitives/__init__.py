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
    VolEgg
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

#from .gdf import GDF
from .heart import Heart
from .platonic import PlatonicSolid
from .vbox import VolBox
from .vcapsule import VolCapsule
from .vcone import VolCone
from .vcylinder import VolCylinder
from .vegg import VolEgg
from .vellipsoid import VolEllipsoid
from .vextrusion import VolExtrusion
from .vplane import VolPlane
from .vpolyhedron import VolPolyhedron
from .vsphere import VolSphere
from .vtorus import VolTorus

__all__ = [
 #   'GDF',
    'Heart',
    'PlatonicSolid',
    'VolBox',
    'VolCapsule',
    'VolCone',
    'VolCylinder',
    'VolEgg',
    'VolEllipsoid',
    'VolExtrusion',
    'VolPlane',
    'VolPolyhedron',
    'VolSphere',
    'VolTorus'
]
