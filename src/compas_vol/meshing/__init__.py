"""
********************************************************************************
compas_vol.meshing
********************************************************************************

.. currentmodule:: compas_vol.meshing

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OctNode
    Octree

"""
from .octree import OctNode
from .octree import Octree

__all__ = [name for name in dir() if not name.startswith('_')]
