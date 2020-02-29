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
	ImageDraw.floodfill(image_obj,(2*x+2, x+1), (255,255,255,255)) #top
	ImageDraw.floodfill(image_obj,(2*x+2, 3*x+3), (255,255,255,255)) #side
	return image_obj


def create_brick_cube(x, w_sep, h_sep):
	# Create a base
	image_obj = create_cube(x)
	
	# Create a mask
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	
	mask_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_mask_obj = ImageDraw.Draw(mask_obj)
	draw_mask_obj.line([(0, 3*x+3), (2*x+2, 4*x+4), (4*x+4, 3*x+3), (4*x+4, 3*x+3 - h_sep+1), (2*x+1, 4*x+4 - h_sep+1), (0, 3*x+3 - h_sep+1), (0, 3*x+3)], fill=(0,0,0,255))
	del draw_mask_obj
	ImageDraw.floodfill(mask_obj,(2*x+2, 4*x+3), (255,255,255,255)) #side
	np_mask_obj = np.array(mask_obj)
	brick_mask = np.array(Image.new('RGBA',(img_w,img_h),color=(0,0,0,0)))
	staggered_mask = np.array(Image.new('RGBA',(img_w,img_h),color=(0,0,0,0)))
	for i in range(int((x+1)/h_sep)):
		brick_mask += np.roll(np_mask_obj, -(2*i)*h_sep, axis=0)
		staggered_mask += np.roll(np_mask_obj, -(1+2*i)*h_sep, axis=0)
	brick_mask = Image.fromarray(brick_mask)
	staggered_mask = Image.fromarray(staggered_mask)
	
	# Create grids
	brick_grid = np.array(Image.new('RGBA',(img_w,img_h),color=(0,0,0,0)))
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)
	staggered_grid = np.array(Image.new('RGBA',(img_w,img_h),color=(0,0,0,0)))
	staggered_grid[:,w_sep/2::w_sep, 3] = 255
	staggered_grid = Image.fromarray(staggered_grid)
	
	# Create 1st brick layer
	brick_layer = create_cube(x)
	for i in range(int((x+1)/h_sep)+1):
		brick_layer.paste(brick_layer, (0, -i*h_sep), image_obj)
	brick_layer.paste(brick_grid, (0, 0), brick_grid)
	#brick_layer.putalpha(brick_mask.split()[-1])
	
	# Create 2nd staggered brick layer
	brick_staggered = create_cube(x)
	for i in range(int((x+1)/h_sep)+1):
		brick_staggered.paste(brick_staggered, (0, -i*h_sep), image_obj)
	brick_staggered.paste(staggered_grid, (0, 0), staggered_grid)
	
	# Combine
	#for i in range(int((x+1)/h_sep)):
	image_obj.paste(brick_layer, (0,0), brick_mask)
	image_obj.paste(brick_staggered, (0,0), staggered_mask)
	
	
	return image_obj


def create_brick_cylinder(x, w_sep, h_sep):
	# Create a base
	image_obj = create_cylinder(x)
	
	# Create a mask
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	x_orig = int((x+1) / np.sqrt(2))
	
	mask_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_mask_obj = ImageDraw.Draw(mask_obj)
	draw_mask_obj.arc([(2*x+2 - 2*x_orig, x+1 - x_orig), (2*x+2 + 2*x_orig, x+1 + x_orig)], 0, 180, fill=(0,0,0,255))
	draw_mask_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig), (2*x+2 + 2*x_orig, 3*x+3 + x_orig)], 0, 180, fill=(0,0,0,255))
	draw_mask_obj.line([(2*x+2 - 2*x_orig, x+1), (2*x+2 - 2*x_orig, 3*x+3)], fill=(0,0,0,255))
	draw_mask_obj.line([(2*x+2 + 2*x_orig, x+1), (2*x+2 + 2*x_orig, 3*x+3)], fill=(0,0,0,255))
	del draw_mask_obj
	ImageDraw.floodfill(mask_obj,(2*x+2, 3*x+3), (255,255,255,255)) #side
	
	# Create 1st brick layer
	brick_grid = np.array(Image.new('RGBA',(img_w,img_h),color=(0,0,0,0)))
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)
	brick_1 = create_cylinder(x)
	brick_1.paste(brick_grid, (0, 0), brick_grid)
	
	# Create 2nd staggered brick layer
	
	# Combine
	
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
	x = 32
	# Base unit
	create_cube(x).save("test_cube.png")
	create_cylinder(x).save("test_cylinder.png")
	create_brick_cylinder(x, 4, 2).save("test_brick_cylinder.png")
	create_brick_cube(x, 12, 8).save("test_brick_cube.png")

	# Hello world
	tiles = [None, create_brick_cube(x,12, 8), create_cylinder(x)]

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
	tile3D(hollow_pattern, tiles, x).save("hollow.png")

