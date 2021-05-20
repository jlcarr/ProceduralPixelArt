from PIL import Image, ImageDraw, ImageOps
import numpy as np
from primitives import *


def leaf(s, orientation=0):
	img_h = s//8
	img_w = s//8
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	print(img_h,img_w)
	ang = np.radians(30)
	
	bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), orientation)
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), np.pi/2+ang, angle_max = 2*np.pi-ang, angle_min = np.pi-ang)
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, img_h/4), np.pi/2-ang, angle_max = np.pi+ang, angle_min = ang)
	
	
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, 3*img_h/8), 0)
	#bresenham_ellipse(image_obj, (img_w//2, img_h//2), (img_w/2, 3*img_h/8), np.pi/2-ang, angle_max = np.pi+ang, angle_min = ang)
	#flip = ImageOps.mirror(image_obj)
	#image_obj.paste(flip, (0,0), mask=flip)
	ImageDraw.floodfill(image_obj,(img_w//2, img_h//2), (255,255,255,255))
	
	#brick_staggered.paste(brick_grid, ((w_sep+1)//2, 0), mask=brick_grid)
	del draw_obj
	return image_obj



def create_tree(s, steps=6):
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
	print(instructions)
	
	# Draw the instructions
	step_length = s/6
	turning_angle = np.radians(20)
	state_stack = []
	pos = (2*s+2, 4*s+4)
	angle = -np.radians(90)
	width = s/10
	dwidth = width/steps/2/1.5

	for c in instructions:
		if c == "F":
			new_x = step_length*np.cos(angle)
			new_y = step_length*np.sin(angle)
			new_pos = (pos[0]+new_x, pos[1]+new_y)
		
			dx = width*np.cos(angle-np.radians(90))
			dy = width*np.sin(angle-np.radians(90))
			pos_l = (pos[0]+dx, pos[1]+dy)
			pos_r = (pos[0]-dx, pos[1]-dy)
			width -= dwidth
			width = max(0, width)
			dx = width*np.cos(angle-np.radians(90))
			dy = width*np.sin(angle-np.radians(90))
			new_pos_l = (new_pos[0]+dx, new_pos[1]+dy)
			new_pos_r = (new_pos[0]-dx, new_pos[1]-dy)

			#draw_obj.line([pos, new_pos], fill=(0,0,0,255))
			draw_obj.polygon([pos_r, pos_l, new_pos_l, new_pos_r], fill=(255,255,255,255))
			draw_obj.line([pos_r, new_pos_r], fill=(0,0,0,255))
			draw_obj.line([pos_l, new_pos_l], fill=(0,0,0,255))
			
			pos = new_pos
			
			if width < 4*dwidth:
				leafer = leaf(s, orientation=-angle)
				image_obj.paste(leafer, (int(pos[0] - s/16), int(pos[1] - s/16)), mask=leafer)
		elif c == "+":
			angle += turning_angle
		elif c == "-":
			angle -= turning_angle
		elif c == "[":
			state_stack.append((pos, angle, width))
		elif c == "]":
			pos, angle, width = state_stack.pop()
		#print(pos, angle)

	del draw_obj
	return image_obj


if __name__ == "__main__":
	#s = 120
	#l=4
	s = 50
	create_tree(s).save('./images/tree.png')

	leaf(s).save('./images/leaf.png')

