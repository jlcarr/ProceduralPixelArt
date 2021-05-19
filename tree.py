from PIL import Image, ImageDraw
import numpy as np
from primitives import *


def create_tree(s):
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
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	L = {
		"X": "F+[[X]-X]-F[-FX]+X",
		"F": "FF"
	}
	step_length = s/8
	
	def rewrite_L_system(axiom, steps):
		instructions = L[axiom]
		new_instructions = ""
		for c in instructions:
			if c in L and steps>0:
				new_instructions += rewrite_L_system(c, steps-1)
			else:
				new_instructions += c
		return new_instructions
		
	instructions = rewrite_L_system("X", 2)
	print(instructions)
	
	# Draw the instructions
	state_stack = []
	pos = (2*s+2, 2*s+2)
	angle = -np.radians(90-25)

	for c in instructions:
		if c == "F":
			new_x = int(np.round(step_length*np.cos(angle)))
			new_y = int(np.round(step_length*np.sin(angle)))
			new_pos = (pos[0]+new_x, pos[1]+new_y)
			draw_obj.line([pos, new_pos], fill=(0,0,0,255))
			pos = new_pos
		elif c == "+":
			angle -= np.radians(25)
		elif c == "-":
			angle += np.radians(25)
		elif c == "[":
			state_stack.append((pos, angle))
		elif c == "]":
			pos, angle = state_stack.pop()
		#print(pos, angle)

	del draw_obj
	return image_obj


if __name__ == "__main__":
	#s = 120
	#l=4
	s = 50
	create_tree(s).save('./images/tree.png')

