# ProceduralPixelArt
Tools for procedural generation of isometric pixel art.

## Description
### The Projection
The projection used is actually NOT an isometric projection, it is a related but slightly different type of axonometric projection: **dimetric projection**.  
This can be seen by examining the drawing of cubes: the vertical axis shorter than those in horizontal plane (which are identical).  
#### Mathematics
The projection matrix can be derived easily from the unit-cube:

![\begin{bmatrix}1&0&-1\\-1&2&-1\end{bmatrix}](https://render.githubusercontent.com/render/math?math=%5Cbegin%7Bbmatrix%7D1%260%26-1%5C%5C-%5Cfrac%7B1%7D%7B2%7D%261%26-%5Cfrac%7B1%7D%7B2%7D%5Cend%7Bbmatrix%7D)

The nullspace of which is:

![\left\{\begin{bmatrix}1\\1\\1\end{bmatrix}\right\}](https://render.githubusercontent.com/render/math?math=%5Cleft%5C%7B%5Cbegin%7Bbmatrix%7D1%5C%5C1%5C%5C1%5Cend%7Bbmatrix%7D%5Cright%5C%7D)

Which makes logical sense. 

### Included Generators
#### Primitives
- Lines (use PIL's `ImageDraw.line`)
- Ellipses and elliptical arcs (`Brensenham_ellipse`)
- Cubic frame `add_frame`
- Cube `create_cube`
- Cylinder `create_cylinder`
- Sphere `create_sphere`
#### Building Blocks
- Brick Cube
- Brick Cylinder
- Platform
- Stairs
#### Layout
- `Tile2D`
- `Tile3D`

### Math and Parameters
- **x**: Base measurement.
   - Total image will be `4*x+5` high and `4*x+5` wide
- **l**: The height of each step.
   - The final steps will be correctly proportioned iff `l-1 == x%l` i.e. `x+1` is a multiple of `l`


## Resources
### Pixel Art Drawing
- https://en.wikipedia.org/wiki/Raster_graphics
- https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
- https://cs.brown.edu/research/pubs/theses/masters/1989/dasilva.pdf
### Python Imaging Library (PIL)
- https://pillow.readthedocs.io/en/stable/index.html
- https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
### Projections
- https://en.wikipedia.org/wiki/Axonometric_projection
- https://en.wikipedia.org/wiki/Kernel_(linear_algebra)
