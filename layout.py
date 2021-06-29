from PIL import Image, ImageDraw
import numpy as np




def sprite_sheet(tiles, s):
	side = 4 * s + 5
	
	img_h = len(tiles) * side
	img_w = len(tiles[0]) * side
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	
	for i,row in enumerate(tiles):
		for j,tile in enumerate(row):
			image_obj.paste(tile, (side*j, side*i), tile)
	return image_obj


def tile2D(map, tiles, x):
	h_shift = x+1
	w_shift = 2*x+2

	img_h = (map.shape[0] + map.shape[1] + 2) * h_shift + 1
	img_w = (map.shape[0] + map.shape[1]) * w_shift + 1
	print(img_w,img_h)
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	
	for i_y in np.arange(0, map.shape[0]):
		for i_x in np.arange(0, map.shape[1]):
			tile = tiles[map[i_y, i_x]]
			w_offset = (i_x - i_y) * w_shift + (map.shape[0] - 1) * w_shift
			h_offset = (i_x + i_y) * h_shift
			if tile:
				image_obj.paste(tile, (w_offset, h_offset), tile)
	return image_obj


def tile3D(map, tiles, x):
	h_shift = x+1
	w_shift = 2*x+2

	img_h = (2 * map.shape[0] + map.shape[1] + map.shape[2]) * h_shift + 1
	img_w = (map.shape[1] + map.shape[2]) * w_shift + 1
	print(img_w,img_h)
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	
	for i_z in range(map.shape[0]):
		for i_y in range(map.shape[1]):
			for i_x in range(map.shape[2]):
				tile = tiles[map[i_z, i_y, i_x]]
				w_offset = (i_x - i_y) * w_shift + (map.shape[1] - 1) * w_shift
				h_offset = (i_x + i_y - 2 * i_z) * h_shift + 2 * (map.shape[0] - 1) * h_shift
				if tile:
					image_obj.paste(tile, (w_offset, h_offset), tile)
	return image_obj


if __name__ == "__main__":
	from primitives import *
	from building_blocks import *
	from person import *
	x = 9
	l = 2
	
	# Spritesheet
	tiles = [
		[
			create_cube(x),
			create_cylinder(x),
			create_platform(x, l),
			create_sphere(x)
		],
		[
			create_staircase(x, l, lr=lr, fb=fb)
				for lr in [-1,1]
					for fb in [-1,1]
		],
		[
			create_staircase_platform(x, l, lr=lr, fb=fb)
				for lr in [-1,1]
					for fb in [-1,1]
		]
	]
	sprite_sheet(tiles, x).save("./images/spritesheet.png")
	
	
	# Sticksheet
	tiles = [
		[
			create_stick(x, step=step, orientation=45*orientation)
				for step in range(8)
		]
			for orientation in range(8)
	]
	sprite_sheet(tiles, x).save("./images/sticksheet.png")


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

	#hollow_brick
	x = 9
	h_sep = 5
	w_sep = 8
	tiles = [
		None,
		create_brick_cube(x, w_sep, h_sep),
		create_brick_cylinder(x, w_sep, h_sep)
	]
	tile3D(hollow_pattern, tiles, x).save("./images/hollow_brick.png")

	s=9
	l=2
	tiles = [
		None,
		create_platform(x, l),	
		create_sphere(x)
	]
	IsoMAZEtric_layout = np.array([
		[
			[1]
		],
		[
			[2]
		]
	])
	icon = tile3D(IsoMAZEtric_layout, tiles, s)
	w_offset = (64-icon.size[0])//2 + 1
	h_offset = (64-icon.size[1])//2 + 1
	canvas = Image.new('RGBA', (64,64), color=(0,0,0,0))
	canvas.paste(icon, (w_offset, h_offset))
	canvas.save("./images/IsoMAZEtric_icon.png")
