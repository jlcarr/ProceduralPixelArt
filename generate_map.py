from PIL import Image, ImageDraw
import numpy as np




def create_cube(x):
	# choose x as length
	# top face is 4*x+3 high and 4*x+5 wide
	# total cube is now 4*x+5 high and 4*x+5 wide
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (2*x+1, 2*x+2), (0, x+1)], fill=(0,0,0,255))
	draw_obj.line([(0, x+1), (0, 3*x+3), (2*x+2, 4*x+4), (4*x+4, 3*x+3), (4*x+4, x+1)], fill=(0,0,0,255))
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))
	del draw_obj
	ImageDraw.floodfill(image_obj,(2*x+2, x+1),(255,255,255,255)) #top
	ImageDraw.floodfill(image_obj,(x+1, 2*x+2),(255,255,255,255)) # left
	ImageDraw.floodfill(image_obj,(3*x+3, 2*x+2),(255,255,255,255)) # right
	return image_obj




def create_cylinder(x):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	x_orig = int((x+1) / np.sqrt(2))
	draw_obj.arc([(2*x+2 - 2*x_orig, x+1 - x_orig), (2*x+2 + 2*x_orig, x+1 + x_orig)], 0, 360, fill=(0,0,0,255))
	draw_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig), (2*x+2 + 2*x_orig, 3*x+3 + x_orig)], 0, 180, fill=(0,0,0,255))
	draw_obj.line([(2*x+2 - 2*x_orig, x+1), (2*x+2 - 2*x_orig, 3*x+3)], fill=(0,0,0,255))
	draw_obj.line([(2*x+2 + 2*x_orig, x+1), (2*x+2 + 2*x_orig, 3*x+3)], fill=(0,0,0,255))
	del draw_obj
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
	# Demonstration
	x = 16
	# Base unit
	create_cube(x).save("test_cube.png")
	create_cylinder(x).save("test_cylinder.png")

	# Hello world
	tiles = [None, create_cube(x)]

	hello_pattern = np.array(
		[
			[1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
			[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1]
		]
	)
	tile2D(hello_pattern, tiles, x).save("hello.png")

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
	tile3D(axes_pattern, tiles, x).save("axes.png")

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
			[1, 0, 0, 0, 0, 1],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 1]
		],
		[
			[1, 0, 0, 0, 0, 1],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 1]
		],
		[
			[1, 0, 0, 0, 0, 1],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 1]
		],
		[
			[1, 0, 0, 0, 0, 1],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 1]
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
	tile3D(hollow_pattern, tiles, x).save("hollow.png")

