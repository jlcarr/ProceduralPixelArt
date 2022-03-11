""" Algorithms to draw raster/pixel art, specifically aimed at pieces of buildings
"""
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

from primitives import *




def create_platform(x,l):
	# choose x as length
	# top face is 4*x+3 high and 4*x+5 wide
	# total cube is now 4*x+5 high and 4*x+5 wide
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)

	# Draw outline
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1), (4*x+4, x+1 + 2*l), (2*x+1, 2*x+2 + 2*l), (0, x+1 + 2*l), (0, x+1)], fill=(0,0,0,255))
	# Fill
	ImageDraw.floodfill(image_obj,(2*x+2, 2*+2),(255,255,255,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw front edge
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 2*x+2 + 2*l)], fill=(0,0,0,255))

	del draw_obj

	return image_obj




def create_fillet_small(x, lr=1):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	f,df,xsol,ysol = ellipse_parametric((img_w//2,img_h//2), (x+1, x+1), angle_min=np.pi)
	f,df,xsol,ysol = shear_y_parametric(f,df,xsol,ysol, -1/2*lr, img_w//2)
	f,df,xsol,ysol = translate_parametric(f,df,xsol,ysol, (lr*(x+1), 3*(x+1)//2))
	bresenham_parametric(image_obj, f, df, xsol, ysol)
	
	draw_obj.line([((2+lr)*(x+1), (4*x+4)*5//8), ((1+lr)*(2*x+2), 3*x+3)][::lr], fill=(0,0,0,255))

	# Draw outline
	draw_obj.line([(0, 3*x+3),(0, x+1), (2*x+2, 0), (4*x+4, x+1), (4*x+4, 3*x+3)], fill=(0,0,0,255))
	draw_obj.line([((1-lr)*(2*x+2), 3*x+3), (2*x+2, 4*x+4)][::lr], fill=(0,0,0,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw front edge
	draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))

	del draw_obj
	return image_obj




def create_fillet(x, lr=-1):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	f,df,xsol,ysol = ellipse_parametric((img_w//2,img_h//2), (2*x+2, 2*x+2), angle_min=np.pi + (lr+1)*np.pi/4, angle_max=2*np.pi + (lr-1)*np.pi/4)
	f,df,xsol,ysol = shear_y_parametric(f,df,xsol,ysol, -1/2*lr, img_w//2)
	f,df,xsol,ysol = translate_parametric(f,df,xsol,ysol, (0, 2*x+2))
	bresenham_parametric(image_obj, f, df, xsol, ysol)
	
	draw_obj.line([(2*x+2, 2*x+2), ((1+lr)*(2*x+2), 3*x+3), ((1+lr)*(2*x+2), x+1)][::lr], fill=(0,0,0,255))
	
	# Draw outline
	draw_obj.line([(0, x+1), (2*x+2, 0), (4*x+4, x+1)], fill=(0,0,0,255))
	# Draw upper from edges
	draw_obj.line([(0, x+1), (2*x+1, 2*x+2), (4*x+4, x+1)], fill=(0,0,0,255))
	
	del draw_obj
	return image_obj




def create_staircase(x, l, lr=1, fb=1):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	# Orientation constants
	x_back = (1-lr)*(2*x+2) + lr*(1-fb)*(x+1)
	y_back = 3*x+3 - (1-fb)*(x+1)/2
	x_front = 2*x+2 + lr*(1-fb)*(x+1)
	y_front = 4*x+4 - (1-fb)*(x+1)/2
	# Final step constants
	i_final = x//l -1
	remainder = x+1 - l*(i_final+1)
	
	# Front-Bottom exterior
	draw_obj.line([(0, 3*x+3), (2*x+2, 4*x+4), (4*x+4, 3*x+3)], fill=(0,0,0,255))
	
	if fb > 0:
		#Back-Top exterior
		draw_obj.line([(x_front, 0), ((1+lr)*(2*x+2), x+1)][::lr], fill=(0,0,0,255))
	
		#Back
		for i in range(x//l):
			# Back, horizontal edge
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*(i+1), y_back - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
			# Back, vertical
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*i, y_back - (2+fb)*l*i)], fill=(0,0,0,255))
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), y_back - (2+fb)*l*(i_final+1)), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

		#Fill the color by the hull, right in the middle
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
		
		for i in range(x//l):
			# Concave edge
			draw_obj.line([(x_back + lr*2*l*(i+1), y_back - 3*l*(i+1)), (x_front + lr*2*l*(i+1), y_front - 3*l*(i+1))][::fb*lr], fill=(0,0,0,255))
	else:
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder)][::fb*lr], fill=(0,0,0,255))
		# Back second final step
		draw_obj.line([(x_back + fb*lr*2*l*i_final, y_back - l*((2+fb)*i_final+2)), (x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder)][::fb*lr], fill=(0,0,0,255))

	#Front Top exterior
	draw_obj.line([((1+fb*lr)*(2*x+2), x+1), ((1+fb*lr)*(2*x+2), 3*x+3)], fill=(0,0,0,255))

	for i in range(x//l):
		# Convex edge
		draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2))][::lr], fill=(0,0,0,255))

	if fb < 0:
		# Fill from center
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
		
		#Back Top exterior
		draw_obj.line([((1-lr)*(2*x+2), x+1), (2*x+2, 2*x+2)][::lr], fill=(0,0,0,255))
		# Very Front exterior edge
		draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 4*x+4)], fill=(0,0,0,255))

	# Convex edge, final step
	draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder)][::lr], fill=(0,0,0,255)) #(2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)

	for i in range(x//l):
		# Front, horizontal edge
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*(i+1), y_front - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
		# Front, vertical
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - (2+fb)*l*i)], fill=(0,0,0,255))
	# Front, final step
	draw_obj.line([(x_front + fb*lr*2*l*(i_final+1), y_front - (2+fb)*l*(i_final+1)), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder), ((2+lr+lr*fb)*(x+1), (3-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

	del draw_obj
	return image_obj




def create_staircase_platform(x, l, lr=1, fb=1):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	# Orientation constants
	x_back = (1-lr)*(2*x+2) + lr*(1-fb)*(x+1)
	y_back = 3*x+3 - (1-fb)*(x+1)/2
	x_front = 2*x+2 + lr*(1-fb)*(x+1)
	y_front = 4*x+4 - (1-fb)*(x+1)/2
	# Final step constants
	i_final = x//l -1
	remainder = x+1 - l*(i_final+1)
	
	if fb > 0:
		#Back-Top exterior
		draw_obj.line([(x_front, 0), ((1+lr)*(2*x+2), x+1)][::lr], fill=(0,0,0,255))
		
		# Front-Bottom exterior
		for i in range(x//l):
			# Front, horizontal edge
			draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2) + 2*l), (x_front + fb*lr*2*l*(i+1), y_front - (2+fb)*l*(i+1) + 2*l)][::fb*lr], fill=(0,0,0,255))
			# Front, vertical
			draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2) + 2*l), (x_front + fb*lr*2*l*i, y_front - (2+fb)*l*i + 2*l)], fill=(0,0,0,255))
		# Front, final step
		draw_obj.line([(x_front + fb*lr*2*l*(i_final+1), y_front - (2+fb)*l*(i_final+1) + 2*l), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder + 2*l), ((2+lr+lr*fb)*(x+1), (3-fb)*(x+1)/2 + 2*l)][::fb*lr], fill=(0,0,0,255))
		if lr > 0:
			draw_obj.line([(0, 3*x+3), (2*x+2, 4*x+4)], fill=(0,0,0,255))
		else:
			draw_obj.line([(2*x+2, 4*x+4), (4*x+4, 3*x+3)], fill=(0,0,0,255))

		#Back
		for i in range(x//l):
			# Back, horizontal edge
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*(i+1), y_back - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
			# Back, vertical
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*i, y_back - (2+fb)*l*i)], fill=(0,0,0,255))
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), y_back - (2+fb)*l*(i_final+1)), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

		#Fill the color by the hull, right in the middle
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
		
		for i in range(x//l):
			# Concave edge
			draw_obj.line([(x_back + lr*2*l*(i+1), y_back - 3*l*(i+1)), (x_front + lr*2*l*(i+1), y_front - 3*l*(i+1))][::fb*lr], fill=(0,0,0,255))
	else:
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder)][::fb*lr], fill=(0,0,0,255))
		# Back second final step
		draw_obj.line([(x_back + fb*lr*2*l*i_final, y_back - l*((2+fb)*i_final+2)), (x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder)][::fb*lr], fill=(0,0,0,255))
		

	#Front Top exterior
	draw_obj.line([((1+fb*lr)*(2*x+2), x+1), ((1+fb*lr)*(2*x+2), x+1 + 2*l)], fill=(0,0,0,255))


	for i in range(x//l):
		# Convex edge
		draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2))][::lr], fill=(0,0,0,255))
		if fb < 0:
			if i > 0:
				draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2) + 4*l), (x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2) + 4*l)][::lr], fill=(0,0,0,255))
			draw_obj.line([((1-lr)*(2*x+2), x+1 + 2*l), (2*x+2, 2*x+2 + 2*l)][::lr], fill=(0,0,0,255))
			draw_obj.line([(x_front, y_front), (x_front + fb*lr*2*l, y_front - (2+fb)*l + 2*l)][::fb*lr], fill=(0,0,0,255))

	if fb < 0:
		# Fill from center
		#return image_obj
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
		# Front-Bottom exterior
		for i in range(x//l):
			# Front, horizontal edge
			draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2) + 2*l), (x_front + fb*lr*2*l*(i+1), y_front - (2+fb)*l*(i+1) + 2*l)][::fb*lr], fill=(0,0,0,255))
			# Front, vertical
			if not i:
				continue
			draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2) + 2*l), (x_front + fb*lr*2*l*i, y_front - (2+fb)*l*i + 2*l)], fill=(0,0,0,255))
		# Front, final step
		draw_obj.line([(x_front + fb*lr*2*l*(i_final+1), y_front - (2+fb)*l*(i_final+1) + 2*l), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder + 2*l), ((2+lr+lr*fb)*(x+1), (3-fb)*(x+1)/2 + 2*l)][::fb*lr], fill=(0,0,0,255))

		#Back Top exterior
		draw_obj.line([((1-lr)*(2*x+2), x+1), (2*x+2, 2*x+2)][::lr], fill=(0,0,0,255))
		# Very Front exterior edge
		draw_obj.line([(2*x+2, 2*x+2), (2*x+2, 2*x+2 + 2*l)], fill=(0,0,0,255))

	# Convex edge, final step
	draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder)][::lr], fill=(0,0,0,255)) #(2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)

	for i in range(x//l):
		# Front, horizontal edge
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*(i+1), y_front - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
		# Front, vertical
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - (2+fb)*l*i)], fill=(0,0,0,255))
	# Front, final step
	draw_obj.line([(x_front + fb*lr*2*l*(i_final+1), y_front - (2+fb)*l*(i_final+1)), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder), ((2+lr+lr*fb)*(x+1), (3-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

	del draw_obj
	return image_obj




def create_staircase_thin(x, l, lr=1, fb=1, thickness=0):
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	# Orientation constants
	x_back = (1-lr)*(2*x+2) + lr*(1-fb)*(x+1)
	y_back = 3*x+3 - (1-fb)*(x+1)/2
	x_front = 2*x+2 + lr*(1-fb)*(x+1)
	y_front = 4*x+4 - (1-fb)*(x+1)/2
	# Final step constants
	i_final = x//l -1
	remainder = x+1 - l*(i_final+1)
	
	if fb > 0:
		#Back-Top exterior
		draw_obj.line([(x_front, 0), ((1+lr)*(2*x+2), x+1)][::lr], fill=(0,0,0,255))
	
		# Front-Bottom exterior
		if lr > 0:
			draw_obj.line([(0, 3*x+3), (2*x+2, 4*x+4), (2*x+2+2*l*thickness, 4*x+4), (4*x+4, x+1+3*l*thickness), (4*x+4, x+1)], fill=(0,0,0,255))
		else:
			draw_obj.line([(0, x+1), (0, x+1+3*l*thickness), (2*x+2-2*l*thickness, 4*x+4), (2*x+2, 4*x+4), (4*x+4, 3*x+3)], fill=(0,0,0,255))

		#Back
		for i in range(x//l):
			# Back, horizontal edge
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*(i+1), y_back - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
			# Back, vertical
			draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_back + fb*lr*2*l*i, y_back - (2+fb)*l*i)], fill=(0,0,0,255))
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), y_back - (2+fb)*l*(i_final+1)), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

		#Fill the color by the hull, right in the middle
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+2), (255,255,255,255))
		
		for i in range(x//l):
			# Concave edge
			draw_obj.line([(x_back + lr*2*l*(i+1), y_back - 3*l*(i+1)), (x_front + lr*2*l*(i+1), y_front - 3*l*(i+1))][::fb*lr], fill=(0,0,0,255))
	else:
		# Back final step
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))
		draw_obj.line([(x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder), (x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder)][::fb*lr], fill=(0,0,0,255))
		# Back second final step
		draw_obj.line([(x_back + fb*lr*2*l*i_final, y_back - l*((2+fb)*i_final+2)), (x_back + fb*lr*2*l*(i_final+1) - 2*fb*lr*remainder, y_back - (2+fb)*l*(i_final+1) + fb*remainder)][::fb*lr], fill=(0,0,0,255))

	for i in range(x//l):
		# Convex edge
		draw_obj.line([(x_back + fb*lr*2*l*i, y_back - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2))][::lr], fill=(0,0,0,255))

	if fb < 0:
		# Front-Bottom exterior
		draw_obj.line([((1-lr)*(2*x+2), x+1), ((1-lr)*(2*x+2), x+1+2*l*thickness), ((1+lr)*(2*x+2)-lr*2*l*thickness, 3*x+3+l*thickness), ((1+lr)*(2*x+2), 3*x+3)][::lr], fill=(0,0,0,255))

		# Fill from center
		ImageDraw.floodfill(image_obj,(2*x+2, 2*x+1), (255,255,255,255))
	
		#Back Top exterior
		draw_obj.line([((1-lr)*(2*x+2), x+1), (2*x+2, 2*x+2), (2*x+2, 2*x+2 +2*l*thickness)][::lr], fill=(0,0,0,255))

	# Convex edge, final step
	draw_obj.line([(x_back + fb*lr*2*l*(i_final+1), (1-fb)*(x+1)/2 + fb*remainder), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder)][::lr], fill=(0,0,0,255)) #(2*x+2 - lr*(1-fb)*(x+1), (1-fb)*(x+1)/2)

	for i in range(x//l):
		# Front, horizontal edge
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*(i+1), y_front - (2+fb)*l*(i+1))][::fb*lr], fill=(0,0,0,255))
		# Front, vertical
		draw_obj.line([(x_front + fb*lr*2*l*i, y_front - l*((2+fb)*i+2)), (x_front + fb*lr*2*l*i, y_front - (2+fb)*l*i)], fill=(0,0,0,255))
	# Front, final step
	draw_obj.line([(x_front + fb*lr*2*l*(i_final+1), y_front - (2+fb)*l*(i_final+1)), (x_front + fb*lr*2*l*(i_final+1), (3-fb)*(x+1)/2 + fb*remainder), ((2+lr+lr*fb)*(x+1), (3-fb)*(x+1)/2)][::fb*lr], fill=(0,0,0,255))

	del draw_obj
	return image_obj




def create_brick_cube(x, w_sep, h_sep):
	# Create a base
	image_obj = create_cube(x)
	img_h = 4 * x + 5
	img_w = 4 * x + 5
	
	# Create a mask
	base_mask_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_mask_obj = ImageDraw.Draw(base_mask_obj)
	draw_mask_obj.line([(0, 3*x+2), (2*x+2, 4*x+3), (4*x+4, 3*x+2), (4*x+4, 3*x+2 - h_sep+1), (2*x+1, 4*x+3 - h_sep+1), (0, 3*x+2 - h_sep+1), (0, 3*x+2)], fill=(0,0,0,255))
	del draw_mask_obj
	ImageDraw.floodfill(base_mask_obj,(2*x+2, 4*x+2), (255,255,255,255)) #side
	base_mask_obj = np.array(base_mask_obj)
	# Create brick mask
	brick_mask = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	for i in range((x+1)//h_sep):
		brick_mask += np.roll(base_mask_obj, -(2*i)*h_sep, axis=0)
	brick_mask = Image.fromarray(brick_mask)
	
	# Create grids
	brick_grid = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)

	# Create basic brick layer
	brick_layer = image_obj.copy()
	brick_draw_obj = ImageDraw.Draw(brick_layer)
	for i in range((2*x+2)//h_sep):
		brick_draw_obj.line([(0, 3*x+3 - ((i+1)*h_sep)), (2*x+2, 4*x+4 - ((i+1)*h_sep)), (4*x+4, 3*x+3 - ((i+1)*h_sep))], fill=(0,0,0,255))
	del brick_draw_obj
	brick_staggered = brick_layer.copy()
	brick_layer.paste(brick_grid, (0, 0), mask=brick_grid)
	brick_staggered.paste(brick_grid, ((w_sep+1)//2, 0), mask=brick_grid)
	
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
	for i in range((x+1)//h_sep):
		brick_mask += np.roll(base_mask_obj, -(2*i)*h_sep, axis=0)
	brick_mask = Image.fromarray(brick_mask)
	
	# Create grids
	brick_grid = np.zeros(base_mask_obj.shape, dtype=np.uint8)
	brick_grid[:,::w_sep, 3] = 255
	brick_grid = Image.fromarray(brick_grid)

	# Create basic brick layer
	brick_layer = image_obj.copy()
	for i in range((2*x+2)//h_sep):
		#brick_draw_obj.arc([(2*x+2 - 2*x_orig, 3*x+3 - x_orig - ((i+1)*h_sep)), (2*x+2 + 2*x_orig, 3*x+3 + x_orig - ((i+1)*h_sep))], 0, 180, fill=(0,0,0,255))
		bresenham_ellipse(brick_layer, (2*x+2, 3*x+3 - (i+1)*h_sep), (2*x_orig+2, x_orig), 0, angle_min = np.pi)
	brick_staggered = brick_layer.copy()
	brick_layer.paste(brick_grid, (0, 0), mask=brick_grid)
	brick_staggered.paste(brick_grid, ((w_sep+1)//2, 0), mask=brick_grid)
	
	# Combine
	image_obj.paste(brick_layer, mask=brick_mask)
	image_obj.paste(brick_staggered, (0,-h_sep), mask=brick_mask)
	
	#brick_staggered.putalpha(staggered_mask.split()[-1])
	return image_obj




def rust(image_obj, iters=2, prob=9, clean=True):
	"""Adds a rusting effect to black and while pixel art PIL image object.
	The effect works by computing the number of lrud-neighbors of each cell,
	then turning that cell black (if it wasn't already) with a probability proportional to the number of neighbors.
	This repears for iters iterations.
	Then if clean is True, any pixels with only 1 neighbor are removed.
	"""

	# convert to 1bit, where while=0,black=1 (for math), stored as uint8
	image_array = np.array(image_obj.convert(mode='LA'))
	rust_array = 1 - image_array[:,:,0]//255

	#kern = np.ones((3,3), dtype=np.uint8)
	kern = np.array([[0,1,0],[1,0,1],[0,1,0]], dtype=np.uint8)
	for i in range(iters):
		neighbors = ndimage.convolve(rust_array, kern, mode='constant', cval=0)
		neighbors *= neighbors
		sample = np.random.randint(0, high=prob, size=rust_array.shape, dtype=np.uint8)
		rust_array = rust_array | (neighbors > sample).astype(np.uint8)

	if clean:
		for i in range(iters):
			neighbors = ndimage.convolve(rust_array, kern, mode='constant', cval=0)
			rust_array = rust_array & (neighbors > 1).astype(np.uint8)
		rust_array = rust_array | (1 - image_array[:,:,0]//255)

	# convert back
	rust_array = 1-rust_array
	rust_array *= 255	
	image_obj.paste(Image.fromarray(rust_array), (0,0), mask=image_obj)
	
	return image_obj




if __name__ == "__main__":
	x = 9
	l = 2
	w_sep = 10
	h_sep = 5
	
	add_background(create_fillet(x)).save("./images/test_test_fillet.png")
	
	create_brick_cube(x, w_sep, h_sep).save("./images/brick_cube.png")
	create_brick_cylinder(x, w_sep, h_sep).save("./images/brick_cylinder.png")
	
	create_staircase(x, l).save("./images/test_staircase.png") #x=35, l=35/8
	create_staircase_platform(x, l, fb=1,lr=1).save("./images/test_staircase_platform.png")
	create_platform(x, l).save("./images/test_platform.png")
	
	create_staircase(x, l, fb= 1,lr= 1).save("./images/staircase_rb_sprite.png")
	create_staircase(x, l, fb=-1,lr= 1).save("./images/staircase_rf_sprite.png")
	create_staircase(x, l, fb= 1,lr=-1).save("./images/staircase_lb_sprite.png")
	create_staircase(x, l, fb=-1,lr=-1).save("./images/staircase_lf_sprite.png")

	create_staircase_platform(x, l, fb= 1,lr= 1).save("./images/staircase_platform_rb_sprite.png")
	create_staircase_platform(x, l, fb=-1,lr= 1).save("./images/staircase_platform_rf_sprite.png")
	create_staircase_platform(x, l, fb= 1,lr=-1).save("./images/staircase_platform_lb_sprite.png")
	create_staircase_platform(x, l, fb=-1,lr=-1).save("./images/staircase_platform_lf_sprite.png")

	create_staircase_thin(x, l, fb= 1,lr= 1).save("./images/staircase_thin_rb_sprite.png")
	create_staircase_thin(x, l, fb=-1,lr= 1).save("./images/staircase_thin_rf_sprite.png")
	create_staircase_thin(x, l, fb= 1,lr=-1).save("./images/staircase_thin_lb_sprite.png")
	create_staircase_thin(x, l, fb=-1,lr=-1).save("./images/staircase_thin_lf_sprite.png")

	x = 19
	w_sep = 16
	h_sep = 10
	l = 4
	rust(create_brick_cube(x, w_sep, h_sep)).save("./images/rusted_brick_cube.png")
	rust(create_brick_cylinder(x, w_sep, h_sep)).save("./images/rusted_brick_cylinder.png")
	rust(create_brick_cube(x, w_sep, h_sep)).save("./images/rusted_brick_cube.png")
	rust(create_staircase(x, l, fb= 1,lr= 1)).save("./images/rusted_staircase_rb_sprite.png")
	rust(create_staircase(x, l, fb=-1,lr= 1)).save("./images/rusted_staircase_rf_sprite.png")
	rust(create_staircase(x, l, fb= 1,lr=-1)).save("./images/rusted_staircase_lb_sprite.png")
	rust(create_staircase(x, l, fb=-1,lr=-1)).save("./images/rusted_staircase_lf_sprite.png")
