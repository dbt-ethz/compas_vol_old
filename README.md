# compas_vol

## Volumetric Modelling

volumetric modeling with signed distance functions

## Installation Instructions

- [compas_vol](https://dbt-ethz.github.io/compas_vol/) is an [extension package](https://compas-dev.github.io/packages.html) built on top of [compas core](https://compas-dev.github.io).
- To get started, I recommend you create a separate environment in an Anaconda Python 3.7 installation. The details are described here: https://compas-dev.github.io/main/gettingstarted/installation.html
- With the newly created environment active, make sure you have git installed. If not, in the terminal (Mac) or Anaconda Prompt (Win) run `conda install git`.
- Then install `compas_vol` directly from source, running `pip install git+https://github.com/dbt-ethz/compas_vol`
- The example notebooks use [meshplot](https://skoch9.github.io/meshplot/) for isosurfacing and mesh display. Install it with `conda install meshplot`
- Some also use [ipyvolume](https://ipyvolume.readthedocs.io/en/latest/index.html). Install it with `conda install -c conda-forge ipyvolume`

## Example

```python
from compas.geometry import Box, Frame, Point
from compas_vol.primitives import VolBox
import numpy as np

box = Box(Frame(Point(0, 0, 0), [1, 0.2, 0], [-0.1, 1, 0]), 20, 15, 15)
vb = VolBox(box, 3.0)

x, y, z = np.ogrid[-15:15:60j, -15:15:60j, -15:15:60j]
d = vb.get_distance_numpy(x, y, z)
```

## Functionality

All the objects have a `get_distance` function, a lot of them also have a faster `get_distance_numpy` function. The following table gives an overview:

Folder | Class | Single point distance | Numpy available
--- | --- | --- | ---
Primitives | VolBox | √ | √
" | VolCapsule | √ | √
" | VolCone | √ | X
" | VolEllipsoid | √ | √
" | VolExtrusion | √ | X
" | Heart | √ | X
" | GDF | X | X
" | VolPlane | √ | √
" | VolPolyhedron | √ | √
" | VolSphere | √ | √
" | VolTorus | √ | √
Combinations | Intersection | √ | √
" | Subtraction | √ | √
" | Union | √ | √
" | Morph | √ | √
" | SmoothIntersection | √ | √
" | SmoothSubtraction | √ | √
" | SmoothUnion | √ | √
Modifications | Blur | X | √
" | Overlay | √ | √ (but missing import)
" | MultiShell | √ | √
" | Shell | √ | √
" | Transformation | √ | √
" | Twist | √ | √
Microstructure | Lattice | √ | √
" | TPMS | √ | √
" | TPMSPolar | √ | √
" | Voronoi | √ | X
Meshing | Octree | √ | X
Analysis | Gradient | √ | √
