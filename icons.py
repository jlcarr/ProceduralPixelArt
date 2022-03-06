from PIL import Image, ImageDraw
from primitives import *
import numpy as np


def draw_marker(s):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)	
	
	arrow_w = s//2

	draw_obj.line([(2*s+2, 3*s+3), (2*s+2 -arrow_w, 3*s+3 -arrow_w),  
		(2*s+2 -arrow_w//2,  3*s+3 -arrow_w), (2*s+2 -arrow_w//2,  2*s+2 -arrow_w),
		(2*s+2 +arrow_w//2,  2*s+2 -arrow_w), (2*s+2 +arrow_w//2,  3*s+3 -arrow_w),
		(2*s+2 +arrow_w, 3*s+3 -arrow_w), (2*s+2, 3*s+3)], fill=(0,0,0,255))
	ImageDraw.floodfill(image_obj,(2*s+2, 2*s+2),(255,255,255,255))	

	del draw_obj
	return image_obj


def draw_moon(s, phase=4):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)	

	curve = (img_w-1) * (4 - phase%4) // 4
	curve_dist = int(np.abs(2*s+2-curve))
	curve_rot = np.pi/2 + np.pi*float(phase%4==1)
	fill = curve//2 if phase < 4 else (img_w-1+curve)//2

	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (2*s+2, 2*s+2), 0)
	ImageDraw.floodfill(image_obj,(2*s+2, 2*s+2), (255,255,255,255))
	
	if curve_dist > 0:
		bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (2*s+2, curve_dist), curve_rot, angle_max=np.pi)
	else:
		draw_obj.line([(2*s+2, 0), (2*s+2, 4*s+4)], fill=(0,0,0,255))
	ImageDraw.floodfill(image_obj,(fill, 2*s+2), (0,0,0,255))

	#if curve_dist > 0:
	#	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (2*s+2, curve_dist), curve_rot, angle_max=np.pi, color=(255,255,255,255))
	#bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (2*s+2, 2*s+2), 0)

	del draw_obj
	return image_obj


def draw_sound_icon(s):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA', (img_w,img_h), color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)

	half = (s+1)//2
	draw_obj.polygon([(2*s+2,s+1), (2*s+2, 3*s+3), (2*s+2-half,3*s+3-half), (2*s+2-half,s+1+half)], outline='black', fill='black')
	draw_obj.rectangle([(s+1,s+1+half), (2*s+2-half,3*s+3-half)], outline='black', fill='black')

	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (s+1, s+1), -np.pi/2, angle_min=np.pi/4, angle_max=3*np.pi/4)
	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (half, half), -np.pi/2, angle_min=np.pi/4, angle_max=3*np.pi/4)
	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (s+1+half, s+1+half), -np.pi/2, angle_min=np.pi/4, angle_max=3*np.pi/4)

	del draw_obj
	return image_obj


def add_prohibition_sign(s, image_obj):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	draw_obj = ImageDraw.Draw(image_obj)

	diag = int(img_h/np.sqrt(2)/2)
	draw_obj.line([(img_w//2-diag,img_h//2+diag),(img_w//2+diag,img_h//2-diag)], fill='black')
	draw_obj.line([(img_w//2-diag,img_h//2+diag+1),(img_w//2+diag,img_h//2-diag+1)], fill=(0,0,0,0))
	draw_obj.line([(img_w//2-diag,img_h//2+diag-1),(img_w//2+diag,img_h//2-diag-1)], fill=(0,0,0,0))

	bresenham_ellipse(image_obj, (2*s+2, 2*s+2), (2*s+2, 2*s+2), 0)
	
	del draw_obj
	return image_obj


if __name__ == "__main__":
	s = 9
	size = 4*s+5
	draw_marker(s).save("./images/marker.png")
	draw_moon(s//2, phase=1).save("./images/moon.png")
	draw_sound_icon(s//2).save("./images/sound_icon.png")
	add_prohibition_sign(s//2, draw_sound_icon(s//2)).save("./images/sound_off_icon.png")

	anim_frames = []
	for phase in range(8):
		frame = draw_moon(s, phase=phase)
		canvas = Image.new(mode='RGBA',size=(size,size), color='white')
		canvas.paste(frame, (0,0), mask=frame)
		anim_frames.append(canvas)
	anim_frames[0].save(fp='./images/moon_phases.gif', format='GIF', append_images=anim_frames[1:], save_all=True, duration=200, loop=0)

