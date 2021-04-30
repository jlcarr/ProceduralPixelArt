from PIL import Image, ImageDraw
import numpy as np
from math import floor
from primitives import *


def create_stick(s, step=-1, orientation=0):
	"""draws a stick person with a walk animation
	"""
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)
	
	peak = project_to_pixel(s, 0, 0.85, 0, y_rot=orientation)
	#head
	head = project_to_pixel(s, 0, 0.85, 0, y_rot=orientation)
	r = int(0.15*(s+1))
	bresenham_ellipse(image_obj, head,(r,r),0)
	ImageDraw.floodfill(image_obj, (int(head[0]),int(head[1])),(255,255,255,255))
	
	#body
	neck = project_to_pixel(s, 0, 0.7, 0, y_rot=orientation)
	groin = project_to_pixel(s, 0, 0, 0, y_rot=orientation)
	draw_obj.line([neck, groin], fill=(0,0,0,255))
	
	
	# walk computations
	stance = 0.1
	knee_height = -0.5
	stride = 0.2
	if step >=0:
		#cycle_len = 8
		# 4/cycle_len * abs((step-cycle_len/4) % cycle_len -cycle_len/2) - 1
		stride_phase = [0, 1/2, 1, 1/2, 0, -1/2, -1, -1/2][step]
		# floor(2*step/cycle_len-1/2) - 2*floor(step/cycle_len-1/4)
		l_touch = [1, 1, 0, 0, 0, 0, 0, 1][step]
		# floor(2*step/cycle_len+1/2) - 2*floor(step/cycle_len+1/4)
		r_touch = [0, 0, 0, 1, 1, 1, 0, 0][step]
		# (l_touch)*((step-1)%cycle_len) + (1-l_touch)*(stride_phase/2)
		l_knee_swing = [1/2, 1, 1, 1/2, 0, -1/2, -1, 0][step]
		r_knee_swing = [0, -1/2, -1, 0, 1/2, 1, 1, 1/2][step]
	else:  #standing still
		stride_phase = 0
		l_touch = 0
		r_touch = 0
		l_knee_swing = 0
		r_knee_swing = 0
	
	#legs
	#left leg
	l_knee = project_to_pixel(s, stance/2, knee_height, stride/2*l_knee_swing, y_rot=orientation)
	l_foot = project_to_pixel(s, stance, -1+l_touch*stance, stride*stride_phase, y_rot=orientation)
	l_toe = project_to_pixel(s, stance, -1+l_touch*stance, stride*stride_phase + stance, y_rot=orientation)
	draw_obj.line([groin, l_knee, l_foot, l_toe], fill=(0,0,0,255))
	#right leg
	r_knee = project_to_pixel(s, -stance/2, knee_height, stride/2*r_knee_swing, y_rot=orientation)
	r_foot = project_to_pixel(s, -stance, -1+r_touch*stance, -stride*stride_phase, y_rot=orientation)
	r_toe = project_to_pixel(s, -stance, -1+r_touch*stance, -stride*stride_phase + stance, y_rot=orientation)
	draw_obj.line([groin, r_knee, r_foot, r_toe], fill=(0,0,0,255))
	
	#arms
	#left arm
	l_arm = project_to_pixel(s, 0.1, 0, -stride_phase*stride/2, y_rot=orientation)
	draw_obj.line([neck, l_arm], fill=(0,0,0,255))
	#right arm
	r_arm = project_to_pixel(s, -0.1, 0, stride_phase*stride/2, y_rot=orientation)
	draw_obj.line([neck, r_arm], fill=(0,0,0,255))
	
	del draw_obj
	return image_obj


def create_person_front(s):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)

	r = s/12

	#Head
	bresenham_ellipse(image_obj, (2*s+2,s + 2*r),(2*r,2*r),0)
	
	#Shoulders
	bresenham_ellipse(image_obj, (2*s+2 - 3*r,s + 5*r),(r,r),0, np.pi, np.pi/2)
	bresenham_ellipse(image_obj, (2*s+2 + 3*r,s + 5*r),(r,r),0, np.pi/2, 0)
	draw_obj.line([(2*s+2 - 3*r,s + 4*r), (2*s+2 + 3*r,s + 4*r)], fill=(0,0,0,255))
	
	# Arms
	draw_obj.line([(2*s+2 - 4*r,s + 5*r), (2*s+2 - 4*r,s + 12*r)], fill=(0,0,0,255))
	draw_obj.line([(2*s+2 + 4*r,s + 5*r), (2*s+2 + 4*r,s + 12*r)], fill=(0,0,0,255))
	
	# Hands
	bresenham_ellipse(image_obj, (2*s+2 - 3*r,s + 12*r),(r,r),0, 2*np.pi, np.pi)
	bresenham_ellipse(image_obj, (2*s+2 + 3*r,s + 12*r),(r,r),0, 2*np.pi, np.pi)
	
	# Sides
	draw_obj.line([(2*s+2 - 2*r,s + 6*r), (2*s+2 - 2*r,s + 23*r)], fill=(0,0,0,255))
	draw_obj.line([(2*s+2 + 2*r,s + 6*r), (2*s+2 + 2*r,s + 23*r)], fill=(0,0,0,255))
	
	# Feet
	bresenham_ellipse(image_obj, (2*s+2 - r,s + 23*r),(r,r),0, 2*np.pi, np.pi)
	bresenham_ellipse(image_obj, (2*s+2 + r,s + 23*r),(r,r),0, 2*np.pi, np.pi)
	
	# Crotch
	draw_obj.line([(2*s+2,s + 14*r), (2*s+2,s + 23*r)], fill=(0,0,0,255))
	
	# Draw outline
	draw_obj.line([(0, s+1), (2*s+2, 0), (4*s+4, s+1), (4*s+4, 3*s+3), (2*s+1, 4*s+4), (0, 3*s+3), (0, s+1)], fill=(0,0,0,255))
	# Draw upper from edges
	draw_obj.line([(0, s+1), (2*s+1, 2*s+2), (4*s+4, s+1)], fill=(0,0,0,255))
	# Draw front edge
	#draw_obj.line([(2*s+2, 2*s+2), (2*s+2, 4*s+4)], fill=(0,0,0,255))

	del draw_obj

	return image_obj



if __name__ == "__main__":
	#s = 120
	#l=4
	#create_person_front(s).save('./images/person.png')
	s = 50
	create_stick(s).save('./images/stick.png')

	size = 4*s+5
	anim_frames = []
	for j in range(8):
		orientation = j*360/8
		for i in range(8):
			frame = create_stick(s, step=i, orientation=orientation)
			canvas = Image.new(mode='RGBA',size=(size,size), color=(255,255,255,0))
			canvas.paste(frame, (0,0), mask=frame)
			anim_frames.append(canvas)

	anim_frames[0].save(fp='./images/stick_walk.gif', format='GIF', append_images=anim_frames[1:],
		save_all=True, duration=200, loop=0)



