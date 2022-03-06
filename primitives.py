""" Implementations of algorithms for drawing raster/pixel art primitives
"""

from PIL import Image, ImageDraw
import numpy as np
from scipy.special import comb, factorial


def project_to_pixel(x, x_coord, y_coord, z_coord, y_rot=0):
	"""Takes xyz coordinates and projects them down to a pixel coordinate
	"""
	projection_matrix = np.array([
		[-1, 0, 1],
		[1/2.0, -1, 1/2.0]
	])
	rotation_matrix = np.array([
		[np.cos(np.radians(y_rot)), 0, -np.sin(np.radians(y_rot))],
		[0, 1, 0],
		[np.sin(np.radians(y_rot)), 0, np.cos(np.radians(y_rot))]
	])
	result = np.array([x_coord, y_coord, z_coord])
	result = rotation_matrix.dot(result)
	result = projection_matrix.dot(result)
	result *= x+1
	result += 2*x+2
	return tuple(np.round(result).astype(int))


def bresenham_ellipse(image_obj, mid_xy, ab, theta, angle_max = 2*np.pi, angle_min = 0, ABCD=None, color=(0,0,0,255)):
	"""Implementation of the Brensenham's line drawing algorithm for elliptic arcs.
	
	This particular implementation is adapted from the uses the pseudocode from DaSilva's master's thesis.
	"""

	def put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color):
		current_angle = np.arctan2(y, x) - theta
		current_angle = current_angle if current_angle >= 0 else current_angle + 2 * np.pi
		current_angle = 2 * np.pi - current_angle
		if (current_angle >= angle_min) and (current_angle <= angle_max):
			try:
				image_obj.putpixel((x + mid_x, y + mid_y), color)
			except:
				pass
	
	mid_x, mid_y = mid_xy
	a,b = ab
	a,b = float(a),float(b)
	theta = -float(theta % np.pi)
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
		put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color)
		put_pixel_arc(image_obj, -x,-y, mid_x,mid_y,  theta, color)
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
		put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color)
		put_pixel_arc(image_obj, -x,-y, mid_x,mid_y,  theta, color)
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
		put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color)
		put_pixel_arc(image_obj, -x,-y, mid_x,mid_y,  theta, color)
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
		put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color)
		put_pixel_arc(image_obj, -x,-y, mid_x,mid_y,  theta, color)
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
	put_pixel_arc(image_obj, x,y, mid_x,mid_y,  theta, color)
	put_pixel_arc(image_obj, -x,-y, mid_x,mid_y,  theta, color)
	return image_obj


def bresenham_parametric(image_obj, f, df, xsol, ysol, color=(0,0,0,255)):
	draw_obj = ImageDraw.Draw(image_obj)

	t = 0
	dt = 0.01 # epsilon to init, shouldn't be needed

	x_prev,y_prev = f(t)
	x_prev = np.ceil(x_prev) if x_prev-np.floor(x_prev) == 0.5 else x_prev
	y_prev = np.ceil(y_prev) if y_prev-np.floor(y_prev) == 0.5 else y_prev
	x_prev,y_prev = round(x_prev),round(y_prev)

	while t <= 1:
		x,y = f(t)
		dx,dy = df(t)
		#print("\nstart")
		#print("t,x,y= ", t,x,y)
		#print("dx,dy= ", dx,dy)
		x = np.ceil(x) if x-np.floor(x) == 0.5 else x
		y = np.ceil(y) if y-np.floor(y) == 0.5 else y
		x,y = round(x),round(y)
		if 0 <= x < image_obj.size[0] and 0 <= y < image_obj.size[1]:
			draw_obj.line([(x_prev,y_prev),(x,y)], fill=color)
			#image_obj.putpixel((x,y), color)
			#print("putpixel=",x,y)
		x_prev,y_prev = x,y
		if np.abs(dx) >= np.abs(dy):
			x += 1 if dx > 0  else -1
			t_new = xsol(x,t)
		else:
			y += 1 if dy > 0  else -1
			t_new = ysol(y,t)
		#print("t_new,x,y=",t_new,x,y)
		if not t_new or np.isnan(t_new) or t_new <= t:
			t_new = t + dt
		dt = t_new - t
		t = t_new
	return image_obj


def bezier_parametric(Ps):
	n = len(Ps)-1
	Ps = [np.array(p) for p in Ps]
	coeffs = [factorial(n)/factorial(n-i) * sum([(-1)**(i+j)*Ps[j]/factorial(j)/factorial(i-j) for j in range(i+1)]) for i in range(n+1)]
	xpoly = np.polynomial.Polynomial([c[0] for c in coeffs])
	ypoly = np.polynomial.Polynomial([c[1] for c in coeffs])

	f = lambda t: sum([coeffs[i] * t**i for i in range(n+1)])
	df = lambda t: sum([(i+1)*coeffs[i+1] * t**i for i in range(n)])
	def parapolysol(x,t0, spoly):
		poly = spoly.copy()
		poly.coef[0] -= x
		sol = poly.roots()
		#print(sol)
		sol = sol[np.isreal(sol)].astype(np.float)
		if not sol.size:
			return None
		return sol[np.argmin(np.abs(sol-t0))]
	xsol = lambda x,t0: parapolysol(x,t0,xpoly)
	ysol = lambda y,t0: parapolysol(y,t0,ypoly)
	return f,df,xsol,ysol


def ellipse_parametric(mid_xy, ab, angle_max = 2*np.pi, angle_min = 0):
	mid_x,mid_y = mid_xy
	a,b = ab

	angle = angle_max - angle_min
	angle_start = angle_min

	f = lambda t: (a*np.cos(angle*t + angle_start) + mid_x, b*np.sin(angle*t + angle_start) + mid_y)
	df = lambda t: (-a*angle*np.sin(angle*t + angle_start), b*angle*np.cos(angle*t + angle_start))
	def xsol(x,t0): 
		angle_t0 = (angle*t0+angle_start) % (2*np.pi)
		angle_sol = np.arccos((x-mid_x)/a)
		angle_sol *= 1 if angle_t0 < np.pi else -1
		sol = ((angle_sol - angle_start) % (2*np.pi)) / angle
		return sol
	def ysol(y,t0): 
		angle_t0 = (angle*t0+angle_start) % (2*np.pi)
		angle_sol = np.arcsin((y-mid_y)/b)
		angle_sol = np.pi-angle_sol if 3*np.pi/2 > angle_t0 >= np.pi/2 else angle_sol
		sol = ((angle_sol - angle_start) % (2*np.pi)) / angle
		return sol
	return f,df,xsol,ysol


def rot_parametric(f,df,xsol,ysol, theta, mid_xy):
	rotation_matrix = np.array([
		[np.cos(theta), -np.sin(theta)],
		[np.sin(theta), np.cos(theta)]
	])
	rot_offset = -rotation_matrix.dot(mid_xy) + mid_xy
	inv_rotation_matrix = np.linalg.inv(rotation_matrix)
	unrot_offset = -inv_rotation_matrix.dot(mid_xy) + mid_xy

	f_rot = lambda t: tuple(rotation_matrix.dot(f(t)) + rot_offset)
	df_rot = lambda t: tuple(rotation_matrix.dot(df(t))) # commutativity of differentials
	def xsol_rot(x,t):
		xp,yp = f_rot(t)
		dxp,dyp = df_rot(t)
		y = yp + (x-xp)*dyp/dxp
		x_unrot,y_unrot = tuple(inv_rotation_matrix.dot((x,y)) + unrot_offset)
		if np.abs(np.cos(theta)) > np.abs(np.sin(theta)):
			t = xsol(x_unrot,t)
		else:
			t = ysol(y_unrot,t)
		return t
	def ysol_rot(y,t):
		xp,yp = f_rot(t)
		dxp,dyp = df_rot(t)
		x = xp + (y-yp)*dxp/dyp
		x_unrot,y_unrot = tuple(inv_rotation_matrix.dot((x,y)) + unrot_offset)
		if np.abs(np.cos(theta)) > np.abs(np.sin(theta)):
			t = ysol(y_unrot,t)
		else:
			t = xsol(x_unrot,t)
		return t
	return f_rot,df_rot,xsol_rot,ysol_rot


def add_ontop_frame(x, image_obj):
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


def add_frame(x, image_obj):
	"""Adds a cubic frame (including back) to a PIL Image object. Useful for debugging.
	"""
	result = Image.new('RGBA',image_obj.size, color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(result)
	
	# Back
	# Draw center edge
	draw_obj.line([(2*x+2, 0), (2*x+2, 2*x+2)], fill=(0,0,0,255))
	# Draw bottom edges
	draw_obj.line([(0, 3*x+3), (2*x+2, 2*x+2), (4*x+4, 3*x+3)], fill=(0,0,0,255))
	
	result.paste(image_obj, (0,0), image_obj)
	
	# Ontop
	# Draw outline
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (4*x+4, 3*x+3), (2*x+1, 4*x+4), (0, 3*x+3), (0, x+1)], fill=(0,0,0,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw front edge
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))
	
	del draw_obj
	return result


def add_background(image_obj, color=(255,255,255,255)):
	"""Adds a background color to images with transparencies
	"""
	result = Image.new('RGBA',image_obj.size,color=color)
	result.paste(image_obj, (0,0), image_obj)
	return result


def create_cube(x):
	"""Creates a basic cube.

	Vertical side length is 2*x+2
	"""
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
	"""Creates a cylinder standing vertically. 

	Size is bounded by the basic cube: Height is 2*x+2, diameter is same as height.
	"""
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
	"""Creates a sphere by drawing a circle: projection stretch is neglected for aesthetics over accuracy.

	Size is bounded by the basic cube: vertical radius is 2*x+2.
	"""
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))

	bresenham_ellipse(image_obj, (2*x+2, 2*x+2), (x+1, x+1), 0)
	ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
	return image_obj


def create_cone(x):
	"""Creates a cone standing vertically.

	Size is bounded by the basic cube: Height is 2*x+2, diameter is same as height.
	"""
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	x_orig = int((x+1) / np.sqrt(2))
	bresenham_ellipse(image_obj, (2*x+2, 3*x+3), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	draw_obj.line([(2*x+2 - 2*x_orig-2, 3*x+3), (2*x+2, x+1), (2*x+2 + 2*x_orig+2, 3*x+3)], fill=(0,0,0,255))
	del draw_obj
	ImageDraw.floodfill(image_obj,(2*x+2, 3*x+3), (255,255,255,255))
	return image_obj




if __name__ == "__main__":
	x = 9
	l = 2
	create_cube(x).save("./images/test_cube.png")
	create_cone(x).save("./images/test_cone.png")
	add_background(add_frame(x, create_cone(x))).save("./images/test_cone_frame.png")
	create_cylinder(x).save("./images/test_cylinder.png")
	add_background(add_frame(x, create_cylinder(x))).save("./images/test_cylinder_frame.png")
	create_sphere(x).save("./images/test_sphere.png")
	add_frame(x, create_sphere(x)).save("./images/test_sphere_frame.png")

	size = 4*x+5

	img = Image.new('RGBA', (size,size), color=(0,0,0,0))
	f,df,xsol,ysol = ellipse_parametric((size//2,size//2), (size//2, size//4)) #, angle_min=np.pi/2, angle_max=3*np.pi/2)
	f,df,xsol,ysol = rot_parametric(f,df,xsol,ysol, theta=np.pi*6/50, mid_xy=(size//2,size//2))
	bresenham_parametric(img, f, df, xsol, ysol)
	img.save("./images/para_ellipse.png")

	Ps = [(0,0),(2*size-2,size-1),(1-size,size-1),(size-1,0)]
	Ps = [(0,size-1),(0,0),(size-1,size-1),(size-1,0)]
	Ps = [(0,size-1),(0,1-size),(size-1,2*(size-1)),(size-1,0)]
	Ps = [(0,size-1),(0,0),(size-1,0),(size-1,size-1)]

	img = Image.new('RGBA', (size,size), color=(0,0,0,0))
	f = lambda t: (10*t, 20*t+5)
	df = lambda t: (10,20)
	ysol = lambda y,t0: (y-5)/20
	xsol = lambda x,t0: x/10
	f,df,xsol,ysol = bezier_parametric(Ps)
	bresenham_parametric(img, f, df, xsol, ysol).save("./images/bezier.png")

	n = 100
	anim_frames = []
	for i in range(n):
		canvas = Image.new(mode='RGBA',size=(size,size), color='white')
		#bresenham_ellipse(canvas, (size//2,size//2), (size//2, size//4), 2*np.pi*i/n)
		para_set = ellipse_parametric((size//2,size//2), (size//2, size//4))
		#para_set = bezier_parametric(Ps)
		para_set = rot_parametric(*para_set, theta=2*np.pi*i/n, mid_xy=(size//2,size//2))
		bresenham_parametric(canvas, *para_set)
		anim_frames.append(canvas)
	anim_frames[0].save(fp='./images/rot.gif', format='GIF', append_images=anim_frames[1:], save_all=True, duration=200, loop=0)
