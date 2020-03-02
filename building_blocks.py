from PIL import Image, ImageDraw
import numpy as np



def bresenham_ellipse(image_obj, mid_xy, ab, theta, angle_max = 2*np.pi, angle_min = 0):
	mid_x, mid_y = mid_xy
	a,b = ab
	theta = -theta
	aSq = a*a
	# focal point
	c = np.sqrt(aSq - b*b)
	# rotated focal point
	Xf = c*np.cos(theta)
	Yf = c*np.sin(theta)
	XfSq = Xf * Xf
	YfSq = Yf * Yf
	
	# Coefficients to G2
	A = aSq - XfSq
	B = -2 * Xf * Yf
	C = aSq - YfSq
	D = aSq * (YfSq - A)
	
	# boudary between region 8 and 1
	k1 = -B/(2*C)
	Xv = np.sqrt(-D/(A + B * k1 + C * k1 * k1))
	Yv = k1 * Xv
	
	# boudary between region 2 and 3
	k2 = -B/(2*A)
	Yh = np.sqrt(-D/(C + B * k2 + A * k2 * k2))
	Xh = k2 * Yh
	
	# boudary between region 1 and 2
	k3 = (2*A - B)/(2*C - B)
	Xr = np.sqrt(-D/(A + B * k3 + C * k3 * k3))
	Yr = k3 * Xr
	if Xr < Yr * k1:
		Yr = - Yr
	
	# boudary between region 3 and 4
	k4 = -(2*A + B)/(2*C + B)
	Xl = np.sqrt(-D/(A + B * k4 + C * k4 * k4))
	Yl = k4 * Xl
	if Xl > Yl * k1:
		Xl = - Xl

	XV = int(round(Xv))
	YV = int(round(Yv))
	YR = int(round(Yr))
	XH = int(round(Xh))
	XL = int(round(Xl))

	# Starting pixel
	x = XV
	y = YV

	# initial point of decition
	Xinit = x - 0.5
	Yinit = y + 1

	Fn = 2*C * Yinit + B * Xinit + C
	Fnw = Fn - 2*A * Xinit - B * Yinit + A - B
	d1 = (A * Xinit * Xinit) + (B * Xinit * Yinit) + (C * Yinit * Yinit) + D

	# Init second order partial derivatives
	Fn_n = 2*C
	Fn_nw = 2*C - B
	Fnw_n = 2*C - B
	Fnw_nw = 2*A - 2*B + 2*C
	Fnw_w = 2*A - B
	Fw_nw = 2*A - B
	Fw_w = 2*A
	Fw_sw = 2*A + B
	Fsw_w = 2*A + B
	Fsw_sw = 2*A + 2*B + 2*C
	Fsw_s = 2*C + B
	Fs_sw = 2*C + B
	Fs_s = 2*C

	# constants used in determining if decision variable has crossed the ellipse
	cross1 = B - A
	cross2 = A - B + C
	cross3 = A + B + C
	cross4 = A + B

	# region 1
	while y < YR:
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
		y += 1
		if (d1  < 0 ) or (Fn - Fnw < cross1):
			d1 += Fn
			Fn += Fn_n
			Fnw += Fnw_n
		else:
			x -= 1
			d1 += Fnw
			Fn += Fn_nw
			Fnw += Fnw_nw

	# region 2
	Fw = Fnw - Fn + A + B + B/2
	Fnw = Fnw + A - C
	d2 = d1 + (Fw - Fn + C)/2 + (A + C)/4 - A
	while x > XH:
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
		x -= 1
		if (d2  < 0 ) or (Fnw - Fw < cross2):
			y += 1
			d2 += Fnw
			Fw += Fw_nw
			Fnw += Fnw_nw
		else:
			d2 += Fw
			Fw += Fw_w
			Fnw += Fnw_w

	# region 3
	d3 = d2 + Fw - Fnw + 2*C - B
	Fw = Fw + B
	Fsw = Fw - Fnw + Fw + 2*C + 2*C - B
	while x > XL:
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
		x -= 1
		if (d3  < 0 ) or (Fsw - Fw > cross3):
			d3 += Fw
			Fw += Fw_w
			Fsw += Fsw_w
		else:
			y -= 1
			d3 += Fsw
			Fw += Fw_sw
			Fsw += Fsw_sw

	# region 4
	Fs = Fsw - Fw - B
	d4 = d3 - Fsw/2 + Fs + A - (A + C - B)/4
	Fsw = Fsw + C - A
	Fs = Fs + C - B/2
	YV = - YV
	while y > YV:
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
		y -= 1
		if (d4  < 0 ) or (Fsw - Fs < cross4):
			x -= 1
			d4 += Fsw
			Fs += Fs_sw
			Fsw += Fsw_sw
		else:
			d4 += Fs
			Fs += Fs_s
			Fsw += Fsw_s
	image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
	image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
	return image_obj



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




def create_fillet(x):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	x_orig = int((x+1) / np.sqrt(2))
	#draw_obj.arc([(2*x+2 - 2*x_orig, 2*x+2 - x_orig), (2*x+2 + 2*x_orig, 2*x+2 + x_orig)], 0, 360) #fill=(0,0,0,255)
	#image_obj = image_obj.rotate(int(np.degrees(np.arctan(3.0/2.0))), Image.NEAREST)
	
	#image_obj = np.array(image_obj)
	#image_obj = np.roll(image_obj, x+1, axis=1)
	#image_obj = np.roll(image_obj, (x+1)/2, axis=0)
	#image_obj = Image.fromarray(image_obj)
	
	draw_obj = ImageDraw.Draw(image_obj)
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (2*x+1, 2*x+2), (0, x+1)], fill=(0,0,0,255))
	draw_obj.line([(0, x+1), (0, 3*x+3), (2*x+2, 4*x+4), (4*x+4, 3*x+3), (4*x+4, x+1)], fill=(0,0,0,255))
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))
	
	bresenham_ellipse(image_obj, (2*x+2, x+1), (2*x_orig+2, x_orig), 0, angle_min = np.pi) # -45*3.14159/180.0
	bresenham_ellipse(image_obj, (x+1, (5*x+5)/2), (2*x_orig+2, x_orig), -np.arctan(3.0/2.0)+0.05)
	bresenham_ellipse(image_obj, (3*x+3, (5*x+5)/2), (2*x_orig+2, x_orig), np.arctan(3.0/2.0)-0.05)

	del draw_obj
	
	return image_obj




def create_cylinder(x):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	x_orig = int((x+1) / np.sqrt(2))
	#draw_obj.arc([(2*x+2 - 2*x_orig, x+1 - x_orig), (2*x+2 + 2*x_orig, x+1 + x_orig)], 0, 360, fill=(0,0,0,255))
	#draw_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig), (2*x+2 + 2*x_orig, 3*x+3 + x_orig)], 0, 180, fill=(0,0,0,255))
	bresenham_ellipse(image_obj, (2*x+2, x+1), (2*x_orig+2, x_orig), 0)
	bresenham_ellipse(image_obj, (2*x+2, 3*x+3), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	draw_obj.line([(2*x+2 - 2*x_orig-2, x+1), (2*x+2 - 2*x_orig-2, 3*x+3)], fill=(0,0,0,255))
	draw_obj.line([(2*x+2 + 2*x_orig+2, x+1), (2*x+2 + 2*x_orig+2, 3*x+3)], fill=(0,0,0,255))
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
	
	base_mask_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_mask_obj = ImageDraw.Draw(base_mask_obj)
	draw_mask_obj.line([(0, 3*x+2), (2*x+2, 4*x+3), (4*x+4, 3*x+2), (4*x+4, 3*x+2 - h_sep+1), (2*x+1, 4*x+3 - h_sep+1), (0, 3*x+2 - h_sep+1), (0, 3*x+2)], fill=(0,0,0,255))
	del draw_mask_obj
	ImageDraw.floodfill(base_mask_obj,(2*x+2, 4*x+2), (255,255,255,255)) #side
	base_mask_obj = np.array(base_mask_obj)
	# Create brick mask
	brick_mask = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	for i in range(int((x+1)/h_sep)):
		brick_mask += np.roll(base_mask_obj, -(2*i)*h_sep, axis=0)
	brick_mask = Image.fromarray(brick_mask)
	
	# Create grids
	brick_grid = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)

	# Create basic brick layer
	brick_layer = image_obj.copy()
	brick_draw_obj = ImageDraw.Draw(brick_layer)
	for i in range(int((2*x+2)/h_sep)):
		brick_draw_obj.line([(0, 3*x+3 - ((i+1)*h_sep)), (2*x+2, 4*x+4 - ((i+1)*h_sep)), (4*x+4, 3*x+3 - ((i+1)*h_sep))], fill=(0,0,0,255))
	del brick_draw_obj
	brick_staggered = brick_layer.copy()
	brick_layer.paste(brick_grid, (0, 0), mask=brick_grid)
	brick_staggered.paste(brick_grid, ((w_sep+1)/2, 0), mask=brick_grid)
	
	# Combine
	image_obj.paste(brick_layer, mask=brick_mask)
	image_obj.paste(brick_staggered, (0,-h_sep), mask=brick_mask)
	
	#brick_staggered.putalpha(staggered_mask.split()[-1])
	return image_obj


def create_brick_cylinder(x, w_sep, h_sep):
	# Create a base
	image_obj = create_cylinder(x)
	
	# Create a mask
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	x_orig = int((x+1) / np.sqrt(2))
	
	base_mask_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	bresenham_ellipse(base_mask_obj, (2*x+2, 3*x+3 - 1), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	bresenham_ellipse(base_mask_obj, (2*x+2, 3*x+3 - h_sep), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	draw_mask_obj = ImageDraw.Draw(base_mask_obj)
	#draw_mask_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig - 1), (2*x+2 + 2*x_orig, 3*x+3 + x_orig - 1)], 0, 180, fill=(0,0,0,255))
	#draw_mask_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig - h_sep), (2*x+2 + 2*x_orig, 3*x+3 + x_orig - h_sep)], 0, 180, fill=(0,0,0,255))
	draw_mask_obj.line([(2*x+2 - 2*x_orig-2, 3*x+3 - 1), (2*x+2 - 2*x_orig-2, 3*x+3 - h_sep+1)], fill=(0,0,0,255))
	draw_mask_obj.line([(2*x+2 + 2*x_orig+2, 3*x+3 - 1), (2*x+2 + 2*x_orig+2, 3*x+3 - h_sep+1)], fill=(0,0,0,255))
	del draw_mask_obj
	ImageDraw.floodfill(base_mask_obj, (2*x+2, 3*x+3 + x_orig - h_sep+2), (255,255,255,255)) #side
	base_mask_obj = np.array(base_mask_obj)
	# Create brick mask
	brick_mask = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	for i in range(int((x+1)/h_sep)):
		brick_mask += np.roll(base_mask_obj, -(2*i)*h_sep, axis=0)
	brick_mask = Image.fromarray(brick_mask)
	
	# Create grids
	brick_grid = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)

	# Create basic brick layer
	brick_layer = image_obj.copy()
	for i in range(int((2*x+2)/h_sep)):
		#brick_draw_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig - ((i+1)*h_sep)), (2*x+2 + 2*x_orig, 3*x+3 + x_orig - ((i+1)*h_sep))], 0, 180, fill=(0,0,0,255))
		bresenham_ellipse(brick_layer, (2*x+2, 3*x+3 - (i+1)*h_sep), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	brick_staggered = brick_layer.copy()
	brick_layer.paste(brick_grid, (0, 0), mask=brick_grid)
	brick_staggered.paste(brick_grid, ((w_sep+1)/2, 0), mask=brick_grid)
	
	# Combine
	image_obj.paste(brick_layer, mask=brick_mask)
	image_obj.paste(brick_staggered, (0,-h_sep), mask=brick_mask)
	
	#brick_staggered.putalpha(staggered_mask.split()[-1])
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
	x = 47
	# Base unit
	create_cube(x).save("test_cube.png")
	create_cylinder(x).save("test_cylinder.png")
	create_brick_cylinder(x, 12, 8).save("test_brick_cylinder.png")
	create_brick_cube(x, 12, 8).save("test_brick_cube.png")
	create_fillet(x).save("test_fillet.png")

	# Hello world
	tiles = [None, create_brick_cube(x, 12, 8), create_brick_cylinder(x, 12, 8)]

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

