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
- Project a point from clipspace to screenspace `project_to_pixel`
- Lines (use PIL's `ImageDraw.line`)
- Ellipses and elliptical arcs (`brensenham_ellipse`)
- Draw on a cube frame (useful for propotioning) `add_frame`
- Cube `create_cube`
- Cylinder `create_cylinder`
- Sphere `create_sphere`
#### Building Blocks
- Brick Cube
- Brick Cylinder
- Platform
- Stairs
- Rust
#### Person
- Draw a still or walking animated stick person `create_stick`
#### Layout
- `sprite_sheet`
- `Tile2D`
- `Tile3D`


### Math and Parameters
- **x**/**s**: Base measurement.
   - Total image will be `4*x+5` high and `4*x+5` wide
- **l**: The height of each step.
   - The final steps will be correctly proportioned iff `(x+1)%l == 0` i.e. `x+1` is a multiple of `l`
- **h_sep**: The height separation for bricks.
   - The bricking will be correctly proportioned iff `2*(x+1)%h_sep == 0`
- **w_sep**: The width separation for bricks.
   - The bricking will be correctly proportioned iff `2*(x+1)%w_sep == 0`

#### Example Values: Small
- **x**: 9
- **l**: 2
- **h_sep**: 5
- **w_sep**: 10

Makes 41x41 images.


### Bresenham's algorithm (approx variant)
Included in this project is a small framework for drawing parametrically define curves.

The idea behind the algorithm is given a continuous (somewhat smooth) parametric curve one can trace it pixel by pixel using the following information:
- `f(t)`: The evaluation of the parametric function at a given `t`, giving coordinates `x,y`
- `df(t)`: The evaluation of the derivative with respect to `t` at a given `t`, giving the velocity `dx,dy`
- `xsol(x,t)`: The inverse of the function for the x-coordinates, given an `x` will find a solution `t` closest to the given `t`
- `ysol(y,t)`: The inverse of the function for the y-coordinates, given an `y` will find a solution `t` closest to the given `t`


## Resources
### Pixel Art Drawing
#### General
- https://en.wikipedia.org/wiki/Raster_graphics
#### Bresenham's Algorithm
- https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
- https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
- https://cs.brown.edu/research/pubs/theses/masters/1989/dasilva.pdf
- http://members.chello.at/~easyfilter/Bresenham.pdf
- http://members.chello.at/~easyfilter/bresenham.html
#### Bezier Curves
- https://en.wikipedia.org/wiki/Bernstein_polynomial
- https://en.wikipedia.org/wiki/B%C3%A9zier_curve
### Python Imaging Library (PIL)
- https://pillow.readthedocs.io/en/stable/index.html
- https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
### Projections
- https://en.wikipedia.org/wiki/Axonometric_projection
- https://en.wikipedia.org/wiki/Kernel_(linear_algebra)
- https://en.wikipedia.org/wiki/Rotation_matrix
