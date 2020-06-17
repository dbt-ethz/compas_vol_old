********************************************************************************
Installation
********************************************************************************

.. highlight:: bash

The installation instructions below assume, that COMPAS core is already installed on the system.
Instructions for how to install this can be found here: https://compas-dev.github.io/main

The easiest way is to install from github directly. You will need ``git`` for this to work. If it's not installed already, run:

::

    $ conda install git

Make sure to have the correct environment activated, where you want ``compas_vol`` to be installed. On Mac in a terminal, run ``conda activate <yourenvname>``, on Windows in the Anaconda Prompt, run ``activate <yourenvname>``, then run the following:

::

    $ pip install git+https://github.com/dbt-ethz/compas_vol

The example notebooks use ipyvolume (https://ipyvolume.readthedocs.io/en/latest/index.html) for isosurfacing and mesh display. Install it with:

::

    $ conda install -c conda-forge ipyvolume