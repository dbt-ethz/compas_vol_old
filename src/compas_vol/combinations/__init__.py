"""
********************************************************************************
compas_vol.combinations
********************************************************************************

.. currentmodule:: compas_vol.combinations

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Union
    Intersection
    Subtraction
    SmoothUnion
    SmoothIntersection
    SmoothSubtraction

"""
from .intersection import *
from .smoothintersection import *
from .smoothsubtraction import *
from .smoothunion import *
from .subtraction import *
from .union import *
from .morph import *

__all__ = [name for name in dir() if not name.startswith('_')]
