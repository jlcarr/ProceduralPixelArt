# ProceduralPixelArt
Tools for procedural generation of isometric pixel art.

## Description
- **x**: Base measurement.
   - Total image will be `4*x+5` high and `4*x+5` wide
- **l**: The height of each step.
   - The final steps will be correctly proportioned iff `l-1 == x%l` i.e. `x+1` is a multiple of `l`


## Resources
- https://en.wikipedia.org/wiki/Raster_graphics
- https://pillow.readthedocs.io/en/stable/index.html
- https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
- https://cs.brown.edu/research/pubs/theses/masters/1989/dasilva.pdf

