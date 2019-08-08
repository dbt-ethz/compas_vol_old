# compas_vol
## Volumetric Modelling

volumetric modelling with function representations

## Installation Instructions

To get started with compas development, I recommend you create a separate environment in an anaconda python 3.7 installation. The details are described here: https://compas-dev.github.io/main/gettingstarted/installation.html

Long story short, the basic steps you need to take are the following:
- preparation
 - `$ conda config --add channels conda-forge`
- ~~create environment for dev and install compas~~
 - ~~`$ conda create -n compas-dev python=3.7 COMPAS`~~
- create a new environment for compas development
 - `$ conda create -n compas-dev python=3.7`
- activate the new environment
 - `$ conda activate compas-dev`
- clone compas core and install it from the local copy
 - `$ git clone git@github.com:compas-dev/compas.git`
 - `$ cd compas`
 - `$ pip install e .`
- navigate to a folder where you want the local copy of `compas_vol`
- clone the repository (you should have gotten an invitation)
 - `$ git clone git@github.com:dbt-ethz/compas_vol.git`
- install the package for the current environment
 - `$ pip install -r requirements-dev.txt`
- furthermore, you will need pyside, opengl, scikit-image and ev. ipyvolume
 - `$ conda install pyopengl`
 - `$ conda install -c conda-forge pyside2`
 - `$ conda install scikit-image`
 - `$ conda install -c conda-forge ipyvolume`
