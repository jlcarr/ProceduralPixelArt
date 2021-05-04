from primitives import *
from building_blocks import *
from layout import *

if __name__ == "__main__":
	x = 9
	l = 2
	h_sep = 5
	w_sep = 10
	

	# Hello world
	tiles = [
		None,
		create_cube(x)
	]
	hello_pattern = np.array(
		[
			[1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
			[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1]
		]
	)
	tile2D(hello_pattern, tiles, x).save("./images/hello_world.png")
	
	
	axes_pattern = np.array([
		[
			[1, 1, 1],
			[1, 0, 0],
			[1, 0, 0]
		],
		[
			[1, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		],
		[
			[1, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]
	])
	tile3D(axes_pattern, tiles, x).save("./images/axes.png")
	
	
	# The stairs_cube
	tiles = [
		None,
		create_cube(x),
		create_staircase(x, l, lr=1),
		create_staircase(x, l, lr=-1),
		create_cylinder(x)
	]
	axes_pattern = np.array([
		[
			[1, 1, 1],
			[1, 1, 1],
			[1, 1, 1]
		],
		[
			[1, 1, 1],
			[1, 4, 2],
			[1, 3, 0]
		],
		[
			[1, 3, 0],
			[2, 4, 0],
			[0, 0, 0]
		]
	])
	tile3D(axes_pattern, tiles, x).save("./images/stairs_cube.png")
	# Rusted
	tiles = [
		None,
		rust(create_brick_cube(2*x+1, 2*w_sep, 2*h_sep)),
		rust(create_staircase(2*x+1, 2*l, lr=1)),
		rust(create_staircase(2*x+1, 2*l, lr=-1)),
		rust(create_brick_cylinder(2*x+1, 2*w_sep, 2*h_sep))
	]
	tile3D(axes_pattern, tiles, 2*x+1).save("./images/rusted_stairs_cube.png")
	
	
	# The stairs_cube 2
	tiles = [
		None,
		create_cube(x),
		create_staircase(x, l, lr=1),
		create_staircase(x, l, lr=-1),
		create_staircase(x, l, lr=1, fb=-1),
		create_staircase(x, l, lr=-1, fb=-1),
		create_cylinder(x)
	]
	axes_pattern = np.array([
		[
			[1, 1, 1],
			[1, 6, 2],
			[1, 0, 0]
		],
		[
			[1, 3, 0],
			[1, 6, 0],
			[1, 0, 0]
		],
		[
			[0, 0, 0],
			[4, 6, 0],
			[1, 0, 0]
		]
	])
	tile3D(axes_pattern, tiles, x).save("./images/stairs_cube2.png")
	# Rusted
	tiles = [
		None,
		rust(create_brick_cube(2*x+1, 2*w_sep, 2*h_sep)),
		rust(create_staircase(2*x+1, 2*l, lr=1)),
		rust(create_staircase(2*x+1, 2*l, lr=-1)),
			rust(create_staircase(2*x+1, 2*l, lr=1, fb=-1)),
		rust(create_staircase(2*x+1, 2*l, lr=-1, fb=-1)),
		rust(create_brick_cylinder(2*x+1, 2*w_sep, 2*h_sep))
	]
	tile3D(axes_pattern, tiles, 2*x+1).save("./images/rusted_stairs_cube2.png")


	# Hollow
	tiles = [
		None,
		create_cube(x),
		create_cylinder(x)
	]
	hollow_pattern = np.array([
		[
			[1, 1, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 1, 1, 1, 1, 1]
		],
		[
			[2, 0, 0, 0, 0, 2],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[2, 0, 0, 0, 0, 2]
		],
		[
			[2, 0, 0, 0, 0, 2],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[2, 0, 0, 0, 0, 2]
		],
		[
			[2, 0, 0, 0, 0, 2],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[2, 0, 0, 0, 0, 2]
		],
		[
			[2, 0, 0, 0, 0, 2],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[2, 0, 0, 0, 0, 2]
		],
		[
			[1, 1, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 1],
			[1, 1, 1, 1, 1, 1]
		]
	])
	tile3D(hollow_pattern, tiles, x).save("./images/hollow.png")

