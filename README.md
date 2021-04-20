# ProceduralPixelArt
Tools for procedural generation of isometric pixel art.

## Description
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
