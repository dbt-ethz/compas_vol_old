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
    SmoothUnionList
    SmoothIntersection
    SmoothSubtraction
    Morph

"""
from .union import Union
from .blend import Blend
from .intersection import Intersection
from .subtraction import Subtraction
from .smoothunion import SmoothUnion
from .smoothunionlist import SmoothUnionList
from .smoothintersection import SmoothIntersection
from .smoothsubtraction import SmoothSubtraction
from .morph import Morph

__all__ = [
    'Union',
    'Blend',
    'Intersection',
    'Subtraction',
    'SmoothUnion',
    'SmoothUnionList'
    'SmoothIntersection',
    'SmoothSubtraction',
    'Morph'
]
