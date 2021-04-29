# compas_vol
## Volumetric Modelling

volumetric modelling with signed distance functions

## Installation Instructions

- [compas_vol](https://dbt-ethz.github.io/compas_vol/) is an [extension package](https://compas-dev.github.io/packages.html) built on top of [compas core](https://compas-dev.github.io).
- To get started, I recommend you create a separate environment in an Anaconda Python 3.7 installation. The details are described here: https://compas-dev.github.io/main/gettingstarted/installation.html
- With the newly created environment active, make sure you have git installed. If not, in the terminal (Mac) or Anaconda Prompt (Win) run `conda install git`.
- Then install `compas_vol` directly from source, running `pip install git+https://github.com/dbt-ethz/compas_vol`
- The example notebooks use [ipyvolume](https://ipyvolume.readthedocs.io/en/latest/index.html) for isosurfacing and mesh display. Install it with `conda install -c conda-forge ipyvolume`

## Functionality

All the objects have a `get_distance` function, a lot of them also have a faster `get_distance_numpy` function. The following table gives an overview:

Folder | Class | Numpy available
--- | --- | ---
Primitives | VolBox | √
" | VolCapsule | √
" | VolCone | X
" | VolEllipsoid | √
" | VolExtrusion | X
" | Heart | X
" | GDF | X
" | VolPlane | √
" | VolPolyhedron | √
" | VolSphere | √
" | VolTorus | √
