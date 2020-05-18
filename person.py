from PIL import Image, ImageDraw
import numpy as np
import building_blocks


def create_person_front(s):
	img_h = 4 * s + 5
	img_w = 4 * s + 5
	image_obj = Image.new('RGBA',(img_w,img_h),color=(0,0,0,0))
	draw_obj = ImageDraw.Draw(image_obj)

	r = s/12

	#Head
	building_blocks.bresenham_ellipse(image_obj, (2*s+2,s + 2*r),(2*r,2*r),0)
	
	#Shoulders
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 - 3*r,s + 5*r),(r,r),0, np.pi, np.pi/2)
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 + 3*r,s + 5*r),(r,r),0, np.pi/2, 0)
	draw_obj.line([(2*s+2 - 3*r,s + 4*r), (2*s+2 + 3*r,s + 4*r)], fill=(0,0,0,255))
	
	# Arms
	draw_obj.line([(2*s+2 - 4*r,s + 5*r), (2*s+2 - 4*r,s + 12*r)], fill=(0,0,0,255))
	draw_obj.line([(2*s+2 + 4*r,s + 5*r), (2*s+2 + 4*r,s + 12*r)], fill=(0,0,0,255))
	
	# Hands
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 - 3*r,s + 12*r),(r,r),0, 2*np.pi, np.pi)
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 + 3*r,s + 12*r),(r,r),0, 2*np.pi, np.pi)
	
	# Sides
	draw_obj.line([(2*s+2 - 2*r,s + 6*r), (2*s+2 - 2*r,s + 23*r)], fill=(0,0,0,255))
	draw_obj.line([(2*s+2 + 2*r,s + 6*r), (2*s+2 + 2*r,s + 23*r)], fill=(0,0,0,255))
	
	# Feet
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 - r,s + 23*r),(r,r),0, 2*np.pi, np.pi)
	building_blocks.bresenham_ellipse(image_obj, (2*s+2 + r,s + 23*r),(r,r),0, 2*np.pi, np.pi)
	
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
	s = 120
	l=4
	create_person_front(s).save('person.png')



