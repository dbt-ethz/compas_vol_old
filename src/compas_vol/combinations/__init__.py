"""
********************************************************************************
compas_vol.combinations
********************************************************************************

.. currentmodule:: compas_vol.combinations

.. autosummary::
    :toctree: generated/
    :nosignatures:

"""
from .intersection import *
from .morph import *
from .smoothintersection import *
from .smoothsubtraction import *
from .smoothunion import *
from .subtraction import *
from .union import *

__all__ = [name for name in dir() if not name.startswith('_')]
