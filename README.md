# compas_vol
## Volumetric Modelling

volumetric modelling with function representations

## PandaRenderer and RayMarchingFactory notes
PandaRenderer, PandaRendererPBR and RayMarchingFactory are classes that provide a real-time visualization environment for the compas and compas-vol shapes. 
Examples for how to use those classes can be found in the folders src/compas_vol/pandaRenderer and src/compas_vol/raymarching.

### PandaRenderer, PandaRendererPBR
The *PandaRenderer* class creates the renderer of the scene (creates window, camera, lights etc.) It extends the ShowBase class from panda3d: https://www.panda3d.org/reference/python/classdirect_1_1showbase_1_1ShowBase_1_1ShowBase.html. 

The *PandaRendererPBR* extends the PandaRenderer, adding PBR environment using the RenderPipeline library: https://github.com/tobspr/RenderPipeline
In order to use the PandaRendererPBR you need to install the RenderPipeline library from this link. 

### RayMarchingFactory
The RayMarchingPactory adds a shader to the PandaRenderer that displays the isosurface of distance fields using raymarching.

#### Compas-vol classes supported in RayMarchingFactory (will change soon)
Primitives: VolSphere, VolBox, VolCylinder, VolTorus
Combinations: Union, Intersection, SmoothUnion
Modifications: Shell

Extras: CSG tree interactive UI, volumetric colored grid with distance values, slicing slider, general purpose slider

#### Ray marching nown issues 
- The python file that is using the RayMarchingFactory class should be stored in the same drive as the raymarching library. For example if you have C: and D:, then you should save both in C: or both in D:. They can be on different folders, but should be on the same drive.
- If you are running on Mac, you will not be able to use the 'post_processing_ray_marching_filter' because they have installed an older version of openGL that has less functionalities available. In that case, you can still use the ray_marching_shader. This does exactly the same as the post-processing filter, only there's no depth buffer available, so there is no depth culling (i.e. the raymarching shapes will always be drawn on top of every other shape in the scene). 
- If you have very low performance when using the raymarching shaders, make sure that your computer uses the GPU for running python (by default it usually doesn't). If you are on windows, download and install the NVIDIA GeForce Experience Driver. Open the NVIDIA Control Panel and go to Manage 3D settings > Progrm Settings. In the dropdown menu 'Select a program to customise' find the python.exe that you are using. The path should look something like: c:/progamdata/anaconda3/python.exe or similar. On the dropdown menu: 'Select a preferred graphics processor for this program' select 'High-performance NVIDIA processor'.  
- At the moment and due to shader memory issues a total of 30 objects and the maximum number of 'children' a combination can have is 20. 


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
   - ~~`$ conda install pyopengl`~~
   - ~~`$ conda install -c conda-forge pyside2`~~
   - `$ conda install scikit-image`
   - `$ conda install -c conda-forge ipyvolume`
