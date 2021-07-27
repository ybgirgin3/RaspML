# This code is designed to take many NDVI images that have been cropped into 512x512 tiles from a larger image of a field. 
# The output is the location of the crop lines in each image. 
# It is difficult to robustly do this for all images, especially the edges of the field. Hence the complexity of the code. 
# The single example image is just to provide a simple demonstration.   

import find_gradient 
import find_lines 
import numpy as np
import matplotlib.pyplot as plt
import scipy 
import sys

from fromCam import get_image

count = 0
simple_example = True # Set to False if you have a set of images that you would like to process
plot_fourier = False #Set to True for 2d fourier transform plot to shown
plot_line_find = True #Set to True for found lines plot to be shown
pixel_value_cutoff = 0.5 #This is the avg pixel value of the lines, below which lines will not be detected. 

#image_paths = []
image_paths = ['example_image.png',"asd.jpeg"]
# resim çek ondan sonra işlem yap
#image_paths.append('example_image.png')
#image_paths.append(get_image())
halfway = int(round(len(image_paths)/2))

#find good estimation of gradient from the middle images (because the middle images are less likely to be edge images)
#for i in range(halfway, halfway + 10):
for i in range(2):
	img = plt.imread(image_paths[i]).astype(float)

	# Using a 2D Fourier Transform, the angle of the lines is detected
	row_distance, source_angle = find_gradient.run_everything(img, plot_fourier)

	if round(source_angle) == 0 or round(source_angle) == -90 or round(source_angle) == 90 or round(source_angle) == 45 or round(source_angle) == -45:
		print('Bad angle:')
		print(source_angle)
	else:
		source_gradient = np.tan(np.deg2rad(source_angle))

		#Find the locations of the lines given the gradient of the lines 
		source_gradient, detected_lines = find_lines.run_everything(img, source_gradient, row_distance, False, pixel_value_cutoff)
		break


print('selected gradient:')
print(source_gradient)

for image in image_paths: #Loop through images provided in image_paths
	print('**--**')
	print('Processing: ' + image)
	img = plt.imread(image).astype(float)
	
	#  Detect the angle of the lines using a 2D Fourier Transform
	row_distance, row_angle = find_gradient.run_everything(img, plot_fourier)

	#checking if the detected row_angle is ok
	if round(row_angle) == 0 or round(row_angle) == -90 or round(row_angle) == 90 or round(row_angle) == 45 or round(row_angle) == -45:
		print('detected bad angle, using source_angle')
		gradient = source_gradient
	else:
		gradient = np.tan(np.deg2rad(row_angle)) 
	
	if count > 0 and improved_gradient and abs(improved_gradient - gradient) < 0.5:
		#Find the locations of the lines given the gradient of the lines 
		improved_gradient, detected_lines = find_lines.run_everything(img, improved_gradient, row_distance, plot_line_find, pixel_value_cutoff)
	else:
		#Find the locations of the lines given the gradient of the lines  
		improved_gradient, detected_lines = find_lines.run_everything(img, gradient, row_distance, plot_line_find, pixel_value_cutoff)

	count += 1
