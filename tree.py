from PIL import Image, ImageDraw, ImageOps
import random
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from primitives import *


def leaf(s, orientation=0):
	img_h = s//8+2
	img_w = s//8+2
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	ang = np.radians(30)
	
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), orientation)
	
	mid_xy = (img_w//2, img_h//2)
	ab = (img_w/2, img_h/4)
	#para_set = ellipse_parametric(mid_xy, ab)
	#para_set = rot_parametric(*para_set, orientation, mid_xy)
	#bresenham_parametric(image_obj, *para_set)
	bresenham_parametric(image_obj, *rot_parametric(*ellipse_parametric(mid_xy, ab), orientation, mid_xy))
	
	
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), np.pi/2+ang, angle_max = 2*np.pi-ang, angle_min = np.pi-ang)
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), np.pi/2-ang, angle_max = np.pi+ang, angle_min = ang)
	
	
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, 3*img_h/8), 0)
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, 3*img_h/8), np.pi/2-ang, angle_max = np.pi+ang, angle_min = ang)
	#flip = ImageOps.mirror(image_obj)
	#image_obj.paste(flip, (0,0), mask=flip)
	ImageDraw.floodfill(image_obj,(img_w//2, img_h//2), (255,255,255,255))
	
	del draw_obj
	return image_obj


def leaf_convex_hull(image_obj, s, leaf_pos, n=750):
	# draw leaves
	# First compute the triangulation of the convex hull, to properly place leaves
	leaf_pos = np.array(leaf_pos)
	hull = ConvexHull(leaf_pos)
	hull_pos = leaf_pos[hull.vertices]
	triangulation = Delaunay(hull_pos)
	
	xmax,xmin = int(hull_pos[:,0].max()), int(hull_pos[:,0].min())
	ymax,ymin = int(hull_pos[:,1].max()), int(hull_pos[:,1].min())

	for i in range(n):
		angle = 2*np.pi*random.random()
		x = random.randrange(xmin,xmax)
		y = random.randrange(ymin,ymax)
		if triangulation.find_simplex((x,y)) < 0:
			continue
		leafer = leaf(s, orientation=angle)
		image_obj.paste(leafer, (x,y), mask=leafer)

	return image_obj


def create_L_tree(s, steps=6):
	"""draws a tree.
	Uses an L-System
	F: draw forward
	+: turn right
	-: turn left
	[: save state
	]: restore state
	"""
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	L = {
		"X": "F+[[X]-X]-F[-FX]+X",
		"F": "FF"
	}
	L = {
		"F": "FF-[-F+F+F]+[+F-F-F]",
	}
	L = {
		"T": "FT-[L]+++[R]--",
		"R": "F-[FL]+++[R]--",
		"L": "F+[FR]--[L]+",
	}

	def rewrite_L_system(axiom, steps):
		instructions = L[axiom]
		new_instructions = ""
		for c in instructions:
			if c in L and steps>0:
				new_instructions += rewrite_L_system(c, steps-1)
			else:
				new_instructions += c
		return new_instructions
		
	instructions = rewrite_L_system("T", steps)
	#print(instructions)
	
	# Draw the instructions
	step_length = s/steps
	turning_angle = np.radians(20)
	state_stack = []
	pos = (2*s+2, 4*s+4)
	angle = -np.radians(90)
	max_width = s/6
	dwidth = max_width/steps/2/1.5


	leaf_pos = []

	F_count = 0
	for c in instructions:
		if c == "F":
			new_x = step_length*np.cos(angle)
			new_y = step_length*np.sin(angle)
			new_pos = (pos[0]+new_x, pos[1]+new_y)
		
			width = max(0, max_width-F_count*dwidth)
			dx = width*np.cos(angle-np.radians(90))
			dy = width*np.sin(angle-np.radians(90))
			pos_l = (pos[0]+dx, pos[1]+dy)
			pos_r = (pos[0]-dx, pos[1]-dy)

			F_count += 1

			width = max(0, max_width-F_count*dwidth)
			dx = width*np.cos(angle-np.radians(90))
			dy = width*np.sin(angle-np.radians(90))
			new_pos_l = (new_pos[0]+dx, new_pos[1]+dy)
			new_pos_r = (new_pos[0]-dx, new_pos[1]-dy)

			#draw_obj.line([pos, new_pos], fill=(0,0,0,255))
			draw_obj.polygon([pos_r, pos_l, new_pos_l, new_pos_r], fill=(255,255,255,255))
			draw_obj.line([pos_r, new_pos_r], fill=(0,0,0,255))
			draw_obj.line([pos_l, new_pos_l], fill=(0,0,0,255))
			
			pos = new_pos
			
			if F_count >= 2*steps:
				leafer = leaf(s, orientation=-angle)
				image_obj.paste(leafer, (int(pos[0] - s/16), int(pos[1] - s/16)), mask=leafer)
				leaf_pos.append(pos)
		elif c == "+":
			angle += turning_angle
		elif c == "-":
			angle -= turning_angle
		elif c == "[":
			state_stack.append((pos, angle, F_count))
		elif c == "]":
			pos, angle, F_count = state_stack.pop()
		#print(pos, angle, F_count, width)
		#print(F_count, width)

	leaf_convex_hull(image_obj, s, leaf_pos)

	del draw_obj
	return image_obj


if __name__ == "__main__":
	#s = 120
	#l=4
	s = 9*5
	#leaf(s, orientation=np.pi/8).save("./images/leaf.png")
	create_L_tree(s).save('./images/L-tree.png')

