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

#from .gdf import GDF
from .heart import Heart
from .vbox import VolBox
from .vcapsule import VolCapsule
from .vcone import VolCone
from .vcylinder import VolCylinder
from .vellipsoid import VolEllipsoid
from .vextrusion import VolExtrusion
from .vplane import VolPlane
from .vpolyhedron import VolPolyhedron
from .vsphere import VolSphere
from .vtorus import VolTorus

__all__ = [
 #   'GDF',
    'Heart',
    'VolBox',
    'VolCapsule',
    'VolCone',
    'VolCylinder',
    'VolEllipsoid',
    'VolExtrusion',
    'VolPlane',
    'VolPolyhedron',
    'VolSphere',
    'VolTorus'
]
