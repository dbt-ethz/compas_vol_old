# compas_vol
## Volumetric Modelling

volumetric modelling with function representations

## Installation Instructions

To get started with compas development, I recommend you create a separate environment in an anaconda python 3.7 installation. The details are described here: https://compas-dev.github.io/main/gettingstarted/installation.html

Long story short, the basic steps you need to take are the following:
1. download and install anaconda for your OS
   - [anaconda.com](https://www.anaconda.com/distribution/), Python 3.7 version
1. preparation
   - `$ conda config --add channels conda-forge`
1. ~~create environment for dev and install compas~~
   - ~~`$ conda create -n compas-dev python=3.7 COMPAS`~~
1. create a new environment for compas development
   - `$ conda create -n compas-dev python=3.7`
1. activate the new environment
   - `$ conda activate compas-dev`
1. navigate to a folder where you want the local copies of **compas** and **compas_vol**
1. clone compas core and install it from the local copy (because not all the features required for compas_vol to work are in the official conda / pip package yet)
   - `$ git clone git@github.com:compas-dev/compas.git`
   - `$ cd compas`
   - `$ pip install -e .`
1. there is a known issue for compas with this installation (planarity/cython)
   - see [this post](https://compas-dev.github.io/main/gettingstarted/knownissues.html) for a fix
1. clone the repository (you should have gotten an invitation)
   - `$ git clone git@github.com:dbt-ethz/compas_vol.git`
1. install the package for the current environment
   - `$ pip install -r requirements-dev.txt`
1. furthermore, you will need pyside, opengl, scikit-image and ev. ipyvolume (will go into requirements.txt)
   - `$ conda install pyopengl`
   - `$ conda install -c conda-forge pyside2`
   - `$ conda install scikit-image`
   - `$ conda install -c conda-forge ipyvolume`
