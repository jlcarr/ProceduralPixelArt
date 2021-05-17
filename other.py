from PIL import Image, ImageDraw
from primitives import *


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


if __name__ == "__main__":
	s = 9
	draw_marker(s).save("./images/marker.png")
