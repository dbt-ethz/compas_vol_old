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
    Morph

"""
from .intersection import Intersection
from .smoothintersection import SmoothIntersection
from .smoothsubtraction import SmoothSubtraction
from .smoothunion import SmoothUnion
from .subtraction import Subtraction
from .union import Union
from .morph import Morph

__all__ = [
    'Intersection',
    'SmoothIntersection',
    'SmoothSubtraction',
    'SmoothUnion',
    'Subtraction',
    'Union',
    'Morph'
]
