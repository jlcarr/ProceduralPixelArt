""" Implementations of algorithms for drawing raster/pixel art primitives
"""

from PIL import Image, ImageDraw
import numpy as np


def project_to_pixel(x, x_coord, y_coord, z_coord):
	"""Takes xyz coordinates and projects them down to a pixel coordinate
	"""
	projection_matrix = np.array([
		[-1, 0, 1],
		[1/2.0, -1, 1/2.0]
	])
	result = projection_matrix.dot(np.array([x_coord, y_coord, z_coord]))
	result *= x+1
	result += 2*x+2
	return tuple(np.round(result).astype(int))


def bresenham_ellipse(image_obj, mid_xy, ab, theta, angle_max = 2*np.pi, angle_min = 0, ABCD=None):
	"""Implementation of the Brensenham's line drawing algorithm for elliptic arcs.
	
	This particular implementation is adapted from the uses the pseudocode from DaSilva's master's thesis.
	"""
	
	mid_x, mid_y = mid_xy
	a,b = ab
	a,b = float(a),float(b)
	theta = -float(theta)
	aSq = a*a
	# focal point
	c = np.sqrt(a*a - b*b)
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
	
	if ABCD:
		A,B,C,D = ABCD
		A,B,C,D = float(A),float(B),float(C),float(D)
	#print(A,B,C,D)
	
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

	#print("XV,YV,YR,XH,XL",XV,YV,YR,XH,XL)
	#print("(Xv,Yv),(Xr,Yr),(Xh,Yh),(Xl,Yl)",(int(Xv),int(Yv)),(int(Xr),int(Yr)),(int(Xh),int(Yh)),(int(Xl),int(Yl)))
	#print("(Xv,Yv),(Xr,Yr),(Xh,Yh),(Xl,Yl)",(Xv,Yv),(Xr,Yr),(Xh,Yh),(Xl,Yl))
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
		#print("reg1: x,y",x,y)
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
			except:
				pass
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
			except:
				pass
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
	#return image_obj

	# region 2
	Fw = Fnw - Fn + A + B + B/2
	Fnw = Fnw + A - C
	d2 = d1 + (Fw - Fn + C)/2 + (A + C)/4 - A
	while x > XH:
		#print("reg2: x,y",x,y)
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
			except:
				pass
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
			except:
				pass
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
		#print("reg3: x,y",x,y)
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
			except:
				pass
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
			except:
				pass
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
		#print("reg4: x,y",x,y)
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
			except:
				pass
		current_angle = np.arctan2(-y, -x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
			except:
				pass
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
	try:
		image_obj.putpixel((x + mid_x, y + mid_y), (0,0,0,255))
		image_obj.putpixel((-x + mid_x, -y + mid_y), (0,0,0,255))
	except:
		pass
	return image_obj




def add_frame(image_obj,x):
	"""Adds a cubic frame on top of a PIL Image object. Useful for debugging.
	"""
	draw_obj = ImageDraw.Draw(image_obj)
	# Draw outline
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (4*x+4, 3*x+3), (2*x+1, 4*x+4), (0, 3*x+3), (0, x+1)], fill=(0,0,0,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw front edge
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))
	del draw_obj
	return image_obj




def create_cube(x):
	# choose x as length
	# top face is 4*x+3 high and 4*x+5 wide
	# total cube is now 4*x+5 high and 4*x+5 wide
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)

	# Draw outline
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (4*x+4, 3*x+3), (2*x+1, 4*x+4), (0, 3*x+3), (0, x+1)], fill=(0,0,0,255))
	# Fill
	ImageDraw.floodfill(image_obj,(2*x+2, 2*+2),(255,255,255,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw front edge
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))

	del draw_obj

	return image_obj




def create_cylinder(x):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	x_orig = int((x+1) / np.sqrt(2))
	bresenham_ellipse(image_obj, (2*x+2, x+1), (2*x_orig+2, x_orig), 0)
	bresenham_ellipse(image_obj, (2*x+2, 3*x+3), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	draw_obj.line([(2*x+2 - 2*x_orig-2, x+1), (2*x+2 - 2*x_orig-2, 3*x+3)], fill=(0,0,0,255))
	draw_obj.line([(2*x+2 + 2*x_orig+2, x+1), (2*x+2 + 2*x_orig+2, 3*x+3)], fill=(0,0,0,255))
	del draw_obj
	ImageDraw.floodfill(image_obj,(2*x+2, x+1), (255,255,255,255)) #top
	ImageDraw.floodfill(image_obj,(2*x+2, 3*x+3), (255,255,255,255)) #side
	return image_obj




def create_sphere(x):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))

	bresenham_ellipse(image_obj, (2*x+2, 2*x+2), (x+1, x+1), 0)
	ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
	return image_obj




if __name__ == "__main__":
	x = 9
	l = 2
	create_cube(x).save("./images/test_cube.png")
	create_cylinder(x).save("./images/test_cylinder.png")
	add_frame(create_cylinder(x), x).save("./images/test_cylinder_frame.png")
	create_sphere(x).save("./images/test_sphere.png")
	add_frame(create_sphere(x), x).save("./images/test_sphere_frame.png")
