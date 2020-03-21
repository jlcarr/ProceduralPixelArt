from PIL import Image, ImageDraw
import numpy as np
import building_blocks
import random

def gen_walk(x_l, y_l, z_l, walk_len=None):
	if not walk_len:
		walk_len = x_l*y_l*z_l/4

	result = -np.ones((x_l, y_l, z_l), dtype=int)
	
	# init position
	x,y,z = (x_l-1, y_l-1, 0)
	result[x,y,z] = 1
	result[x,y,z+1] = 0
	
	# random walk
	for i in range(walk_len):
		moves = []
		# if on a flat step
		if z+1 < z_l and result[x,y,z] == 1 and result[x,y,z+1] == 0:
			# Move Left
			if x > 0 and result[x-1,y,z] in [-1,1] and result[x-1,y,z+1] in [-1,0]:
				moves.append((-1,0,0))
			# Move Right
			if x < x_l-1 and result[x+1,y,z] in [-1,1] and result[x+1,y,z+1] in [-1,0]:
				moves.append((1,0,0))
			# Move Back
			if y > 0 and result[x,y-1,z] in [-1,1] and result[x,y-1,z+1] in [-1,0]:
				moves.append((0,-1,0))
			# Move Front
			if y < y_l-1 and result[x,y+1,z] in [-1,1] and result[x,y+1,z+1] in [-1,0]:
				moves.append((0,1,0))
			# Move Up Left
			if x > 0 and z+2 < z_l and result[x-1,y,z+1] in [-1,3] and result[x-1,y,z+2] in [-1,0]:
				moves.append((-1,0,1))
			# Move Up Right
			if x < x_l-1 and z+2 < z_l and result[x+1,y,z+1] in [-1,5] and result[x+1,y,z+2] in [-1,0]:
				moves.append((1,0,1))
			# Move Up Back
			if y > 0 and z+2 < z_l and result[x,y-1,z+1] in [-1,2] and result[x,y-1,z+2] in [-1,0]:
				moves.append((0,-1,1))
			# Move Up Front
			if y < y_l-1 and z+2 < z_l and result[x,y+1,z+1] in [-1,4] and result[x,y+1,z+2] in [-1,0]:
				moves.append((0,1,1))
		# If on up-left stair
		if z+1 < z_l and result[x,y,z] == 3 and result[x,y,z+1] == 0:
			# Move Left
			if x > 0 and result[x-1,y,z] in [-1,1] and result[x-1,y,z+1] in [-1,0]:
				moves.append((-1,0,0))
			# Move Up Left
			if x > 0 and z+2 < z_l and result[x-1,y,z+1] in [-1,3] and result[x-1,y,z+2] in [-1,0]:
				moves.append((-1,0,1))
		# If on up-back stair
		if z+1 < z_l and result[x,y,z] == 2 and result[x,y,z+1] == 0:
			# Move Front
			if y > 0 and result[x,y-1,z] in [-1,1] and result[x,y-1,z+1] in [-1,0]:
				moves.append((0,-1,0))
			# Move Up Front
			if y > 0 and z+2 < z_l and result[x,y-1,z+1] in [-1,2] and result[x,y-1,z+2] in [-1,0]:
				moves.append((0,-1,1))
		# If on up-right stair
		if z+1 < z_l and result[x,y,z] == 5 and result[x,y,z+1] == 0:
			# Move Right
			if x < x_l-1 and result[x+1,y,z] in [-1,1] and result[x+1,y,z+1] in [-1,0]:
				moves.append((1,0,0))
			# Move Up Right
			if x < x_l-1 and z+2 < z_l and result[x+1,y,z+1] in [-1,5] and result[x+1,y,z+2] in [-1,0]:
				moves.append((1,0,1))
		# If on up-front stair
		if z+1 < z_l and result[x,y,z] == 5 and result[x,y,z+1] == 0:
			# Move Front
			if y < y_l-1 and result[x,y+1,z] in [-1,1] and result[x,y+1,z+1] in [-1,0]:
				moves.append((0,1,0))
			# Move Up Front
			if y < y_l-1 and z+2 < z_l and result[x,y+1,z+1] in [-1,4] and result[x,y+1,z+2] in [-1,0]:
				moves.append((0,1,1))
		
		if not moves:
			break
	
		x_update, y_update, z_update = random.choice(moves)
		print("pos+update")
		print(x,y,z)
		print(x_update, y_update, z_update)
		x += x_update
		y += y_update
		z += z_update
		
		result[x,y,z+1] = 0
		if not z_update:
				result[x,y,z] = 1
		else:
			if x_update == -1:
				result[x,y,z] = 3
			if x_update == 1:
				result[x,y,z] = 5
			if y_update == -1:
				result[x,y,z] = 2
			if y_update == 1:
				result[x,y,z] = 4

	result[result == -1] = 0
	result = np.moveaxis(result, [0,1,2], [2,1,0])
	print(result)
	return result

if __name__ == "__main__":
	s = 35
	l=8
	
	tiles = [
		None,
		building_blocks.create_cube(s),
		building_blocks.create_staircase(s, s/8, lr=1),
		building_blocks.create_staircase(s, s/8, lr=-1),
		building_blocks.create_staircase(s, s/8, lr=1, fb=-1),
		building_blocks.create_staircase(s, s/8, lr=-1, fb=-1),
		building_blocks.create_cylinder(s)
	]
	
	
	axes_pattern = gen_walk(6,6,6)
	
	building_blocks.tile3D(axes_pattern, tiles, s).save("random_walk.png")
