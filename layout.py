from PIL import Image, ImageDraw
import numpy as np




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
	x = 9
	l = 2
	

	# Hello world
	tiles = [
		None,
		create_cube(x, 12, 8)
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

