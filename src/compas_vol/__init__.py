"""
********************************************************************************
compas_vol
********************************************************************************

.. currentmodule:: compas_vol


.. toctree::
    :maxdepth: 1

    compas_vol.primitives
    compas_vol.combinations
    compas_vol.modifications
    compas_vol.microstructures
    compas_vol.analysis

"""

from __future__ import print_function

import os


__author__ = ['Mathias Bernhard <bernhard@arch.ethz.ch>']
__copyright__ = 'Digital Building Technologies - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'bernhard@arch.ethz.ch'
__version__ = '0.1.0'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))


__all__ = ['HOME', 'DATA', 'DOCS', 'TEMP']
