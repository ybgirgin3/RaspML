import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import sys 
from scipy.signal import find_peaks_cwt
import math
import itertools
from random import randint
import operator

# This function converts the array indexes to cartesian coordinates when finding lines, then converts it back. 
# For a 256x256 image, the point [256][0] = [row_index][column_index] is the equivalent of the cartesian point (0,0) = (x,y)
def array_to_cartesian(max_y, start_index):
	#The array index is given in [rows][columns]
	x1 = start_index[1]
	y1 = max_y - start_index[0]
	return x1, y1

def cartesian_to_array(max_y, x1, y1):
	#The array index is given in [rows][columns]
	col_x = x1
	row_y = max_y - y1
	return col_x, row_y

# given a point on the edge of the image, find the point where a line  
# of given gradient intersects the other edge of the image. 
def set_rise_find_run(x1, y1, gradient, max_x, max_y): 
	#Assume rise given start point, find run 
	#gradient = rise/run
	up = False

	if y1 == 0: #on the bottom
		up = True
	elif y1 == max_y: #on the top
		up = False
	elif x1 == 0: #we're on the left wall
		if gradient < 0:
			up = False
		else:
			up = True
	else: #we're on the right wall
		if gradient > 0:
			up = False
		else:
			up = True
	
	if up:
		rise = max_y - y1 #going up, rise is the distance between max_y and y1
		y2 = max_y
	else:
		rise = -y1 #going down, rise is the height of y above 0
		y2 = 0

	run = rise/gradient
	x2 = x1 + np.rint(run) 
	if x2 >= 0 and x2 <= max_x:
		return x2, y2
	else:
		x2, y2 = set_run_find_rise(x1, y1, gradient, max_x, max_y)
		return x2, y2

def set_run_find_rise(x1, y1, gradient, max_x, max_y): 
	right = False
	if x1 == 0: #on the left
		right = True
	elif x1 == max_x: #on the right
		right = False
	elif y1 == 512: #we're on the top 
		if gradient < 0:
			right = True
		else:
			right = False
	else: #we're on the bottom
		if gradient < 0:
			right = False
		else:
			right = True

	if right:
		run = max_x - x1 #going right, run is the difference between max_x and x
		x2 = max_x
	else:
		run = -x1 #going left, run is x1
		x2 = 0

	rise = run*gradient
	y2 = y1 + np.rint(rise)
	if y2 >= 0 and y2 <= max_y:
		return x2, y2
	else:
		print('FAIL2:')
		print('x2, y2:')
		print([x2,y2])
		sys.exit('end index out of bounds.')

#Take gradient, row_distance => return the start indexes
def get_start_indexes(gradient, row_distance, max_x, max_y):
	# Problem: when gradient is very large, very close to 0, and very negative then 
	# number of iterations moving along one edge results in many more crop lines 'crossed'. 
	# so we have to skip pixels moving along edges, the number we have to skip is related to the 
	# ratio of the rise/run = gradient  
	
	start_indexes = []

	inverse_gradient = -1/gradient

	count = 0
	
	if gradient < 0: #If gradient neg, start at bottom left and then move: up and then right  
		count = 0

		for rows in range(1, max_y): # going up the left side
			if gradient < -1: #Then the problem side is the left

				if count % abs(int(round(gradient))) == 0:
					start_index = [max_y - rows,0]
					start_indexes.append(start_index)
			else:
				start_index = [max_y - rows,0]
				start_indexes.append(start_index)
			count += 1
		count = 0

		for columns in range(max_x): # going right across the top
			if gradient > -1: #Then the problem side is the top
				if count % abs(int(round(inverse_gradient))) == 0:
					start_index = [0, columns]
					start_indexes.append(start_index)
			else: 
				start_index = [0, columns]
				start_indexes.append(start_index)
			count += 1
	
	else: #If gradient pos, start at top left and then move: down and then right
		count = 0
		for rows in range(1, max_y): #going down the left side 

			if gradient > 1: #This left side is the problem side
				if count % abs(int(round(gradient))) == 0:
					start_index = [rows,0]
					start_indexes.append(start_index)
			else:
				start_index = [rows,0]
				start_indexes.append(start_index)
			count += 1
		
		count = 0
		for columns in range(max_x): #going right along the bottom 
			if gradient < 1: #This bottom side is the problem side
				if count % abs(int(round(inverse_gradient))) == 0:
					start_index = [max_y, columns]
					start_indexes.append(start_index)
			else:
				start_index = [max_y, columns]
				start_indexes.append(start_index)
			count += 1

	#the first and last indexes (eg. [0,0]) are purposfully not included as they are not needed for the get_line_indexes() algorithm
	
	return start_indexes 

#given start indexes, gradient => return the end indexes
def get_line_indexes(start_indexes, gradient, max_y, max_x):
	line_indexes = []

	for start_index in start_indexes:
		line = []
		x1, y1 = array_to_cartesian(max_y, start_index)
		x2, y2 = set_rise_find_run(x1, y1, gradient, max_x, max_y)
		x2, y2 = cartesian_to_array(max_y, x2, y2)
		end_index = [int(y2), int(x2)]
		line = [start_index, end_index]
		line_indexes.append(line)

	return line_indexes	

#given lines, find avg pixel value along lines
def get_line_values(line_indexes,img):
	num = 500 #This number determines how many coordinates are checked along the line? 
	avg_pixel_values = []
	for line in line_indexes:
		start_index = line[0]
		end_index = line[1]
		x1 = start_index[1]
		y1 = start_index[0]
		x2 = end_index[1]
		y2 = end_index[0]
	
		x, y = np.linspace(x1, x2, num), np.linspace(y1, y2, num)

		# Extract the values along the line, using cubic interpolation
		zi = scipy.ndimage.map_coordinates(np.transpose(img), np.vstack((x,y))) # THIS SEEMS TO WORK CORRECTLY

		avg_pixel_value = np.average(zi)
		avg_pixel_values.append(avg_pixel_value)

	return avg_pixel_values

#given the pixel values => output the locations of the maxima
def get_line_locations(avg_pixel_values):
	peaks = find_peaks_cwt(avg_pixel_values, np.arange(1, 10))
	return peaks


def plot_line_detection(avg_pixel_values, peaks):
	#plotting the estimated peaks against actual peaks 
	num_lines = len(avg_pixel_values)
	x_axis = list(range(num_lines))
	fig0 = plt.figure()
	ax0 = fig0.add_subplot(111)
	ax0.plot(x_axis, avg_pixel_values)
	peak_values = []
	for peak in peaks:
		peak_values.append(avg_pixel_values[peak])

	ax0.plot(peaks, peak_values, 'o')

def write_found_lines(img, detected_lines):#Impose lines over the image and print 

	fig, axes = plt.subplots()
	axes.imshow(img)
	for line in detected_lines:
		x1 = line[0][1]
		y1 = line[0][0]
		x2 = line[1][1]
		y2 = line[1][0]
		axes.plot([x1, x2], [y1, y2], 'ro-')
	axes.axis('off')
	fig.savefig('found_lines.png', bbox_inches='tight')

def plot_found_lines(img, detected_lines):
	fig, axes = plt.subplots()
	axes.imshow(img)
	for line in detected_lines:
		x1 = line[0][1]
		y1 = line[0][0]
		x2 = line[1][1]
		y2 = line[1][0]
		axes.plot([x1, x2], [y1, y2], 'ro-')
	axes.axis('off')
	# fig.savefig('found_lines.png', bbox_inches='tight')
	axes.axis('image')
	
def get_long_line(img, line_indexes, max_x, max_y):
	#Get the first line that is longer than the shortest side 

	len_indexes = len(line_indexes)
	vertical = True
	middle = list(range(int(round(len_indexes/3)),len_indexes - 10))
	length_list = []

	#This value just makes sure we don't get a line too close to a corner, 
	#because that's harder to rotate in improve_line()
	pix_move = 10 

	shortest_side = max_y
	if max_x < max_y:
		shortest_side = max_x
	elif max_x > max_y:
		shortest_side = max_y

	for index in middle:
		line = line_indexes[index]
		
		start_index = line[0]
		end_index = line[1]
		x1 = int(start_index[1])
		y1 = int(start_index[0])
		x2 = int(end_index[1])
		y2 = int(end_index[0])
		
		length = math.sqrt( abs(x1 - x2)*abs(x1 - x2) + abs(y1 - y2)*abs(y1 - y2) )
		if length >= shortest_side:
			return line


#Take a point and generate points within pix_move pixels of that point that are still in the image
def generate_points(point, max_x, max_y):
	pix_move = 7

	x1 = point[1]
	y1 = point[0]
	
	y_points = list(range(y1 - pix_move, y1 + pix_move))
	x_points = list(range(x1 - pix_move, x1 + pix_move))
	y_points_filtered = []
	x_points_filtered = []
	for i in range(2*pix_move):
		
		if (0 < y_points[i] < max_y) and y_points[i] != y1:
			# print(y_points[i])
			y_points_filtered.append(y_points[i])
	for j in range(2*pix_move):
		
		if (0 < x_points[j] < max_x) and x_points[j] != x1:
			x_points_filtered.append(x_points[j])

	all_combinations = list(itertools.product(y_points_filtered, x_points_filtered))

	return all_combinations


def improve_line(long_line, max_x, max_y, img):
	

	if long_line is None:
		print('Long line is None')
		return False

	num = 500
	iterations = 80
	point1 = long_line[0]
	point2 = long_line[1]
	x1 = int(point1[1])
	y1 = int(point1[0])
	x2 = int(point2[1])
	y2 = int(point2[0])

	x, y = np.linspace(x1, x2, num), np.linspace(y1, y2, num)

	# Extract the values along the line, using cubic interpolation
	zi = scipy.ndimage.map_coordinates(np.transpose(img), np.vstack((x,y))) 

	original_avg_pixel_value = np.average(zi)

	points = []
	points1 = generate_points(point1, max_x, max_y)
	points2 = generate_points(point2, max_x, max_y)

	tested_lines = []
	avg_pixel_values = []
	for i in range(iterations):
		try:
			rand_point_1 = points1[randint(0, len(points1)-1)]
		except:
			print(points1)
		try:
			rand_point_2 = points2[randint(0, len(points2)-1)]
		except:
			print('points2:')
			print(points2)
		x1 = int(rand_point_1[1])
		y1 = int(rand_point_1[0])
		x2 = int(rand_point_2[1])
		y2 = int(rand_point_2[0])

		x, y = np.linspace(x1, x2, num), np.linspace(y1, y2, num)

		# Extract the values along the line, using cubic interpolation
		zi = scipy.ndimage.map_coordinates(np.transpose(img), np.vstack((x,y))) # THIS SEEMS TO WORK CORRECTLY

		avg_pixel_value = np.average(zi)
		line = [rand_point_1, rand_point_2]
		tested_lines.append(line)
		avg_pixel_values.append(avg_pixel_value)
	# best_pixel_value = max(avg_pixel_values)
	index, best_pixel_value = max(enumerate(avg_pixel_values), key=operator.itemgetter(1))
	improved_line = tested_lines[index]

	if best_pixel_value > original_avg_pixel_value:

		#Shift to cartesian coordinates
		x1 = improved_line[0][1]
		y1 = max_y - improved_line[0][0]
		x2 = improved_line[1][1]
		y2 = max_y - improved_line[1][0]
		improved_gradient = (y2 - y1)/(x2 - x1)
		return improved_gradient
	else:
		print('No gradient improvement.')
		return False

def normalize(arr):
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

def get_filtered_lines(avg_pixel_values, peaks, pixel_value_cutoff,line_indexes):
	filtered_peaks = []
	detected_lines = []
	running_peak_values = 0
	if len(peaks) == 0:
		return detected_lines, filtered_peaks

	for i in peaks:
		running_peak_values += avg_pixel_values[i]

	avg_peak_value = running_peak_values/len(peaks)

	if avg_peak_value > pixel_value_cutoff: #Then the image is full of good lines, want to detect all peaks
		for peak in peaks:
			detected_lines.append(line_indexes[peak])
		return detected_lines, peaks
	else:
		for peak in peaks:
			peak_value = avg_pixel_values[peak]
			if peak_value > pixel_value_cutoff:
				filtered_peaks.append(peak)

		for peak in filtered_peaks:
			detected_lines.append(line_indexes[peak])

		return detected_lines, filtered_peaks


def run_everything(img, gradient, row_distance, plot_line_find, pixel_value_cutoff):

	img_shape = img.shape
	max_y = img_shape[0]
	max_x = img_shape[1]
	
	#gradient = tan(theta) of the angle from the positive x-axis, with theta in radians 
	# gradient = np.tan(np.deg2rad(row_tilt)) 

	start_indexes = get_start_indexes(gradient, row_distance, max_x, max_y)
	line_indexes = get_line_indexes(start_indexes, gradient, max_y, max_x)
	
	avg_pixel_values = get_line_values(line_indexes,img)
	peaks = get_line_locations(avg_pixel_values) #peaks contains the indices of the peak values 
	
	# Need to remove peaks below a certain value
	detected_lines, filtered_peaks = get_filtered_lines(avg_pixel_values, peaks, pixel_value_cutoff,line_indexes)

	long_line = get_long_line(img, detected_lines, max_x, max_y)
	improved_gradient = improve_line(long_line, max_x, max_y, img)

	if improved_gradient:
		start_indexes = get_start_indexes(improved_gradient, row_distance, max_x, max_y)
		line_indexes = get_line_indexes(start_indexes, improved_gradient, max_y, max_x)
		avg_pixel_values = get_line_values(line_indexes,img)
		peaks = get_line_locations(avg_pixel_values) #peaks contains the indices of the peak values 
		detected_lines = []

		# Need to remove peaks below a certain value
		detected_lines, filtered_peaks = get_filtered_lines(avg_pixel_values, peaks, pixel_value_cutoff,line_indexes)

	if plot_line_find:
		plot_line_detection(avg_pixel_values, filtered_peaks)
		plot_found_lines(img, detected_lines)
		plt.show()
	return improved_gradient, detected_lines

def main_run():
	img = plt.imread('../Media/cropped512/0.png').astype(float)
	row_tilt = -77.905
	row_distance = 17.88

	img_shape = img.shape
	max_y = img_shape[0]
	max_x = img_shape[1]

	#gradient = tan(theta) of the angle from the positive x-axis, with theta in radians 
	gradient = np.tan(np.deg2rad(row_tilt)) 

	# improve_gradient(gradient, max_y, max_x)

	start_indexes = get_start_indexes(gradient, row_distance, max_x, max_y)
	line_indexes = get_line_indexes(start_indexes, gradient, max_y, max_x)
	
	avg_pixel_values = get_line_values(line_indexes,img)
	peaks = get_line_locations(avg_pixel_values) #peaks contains the indices of the peak values 
	detected_lines = []
	for peak in peaks:
		detected_lines.append(line_indexes[peak])

	long_line = get_long_line(img, detected_lines, max_x, max_y)
	improved_gradient = improve_line(long_line, max_x, max_y, img)


	start_indexes = get_start_indexes(improved_gradient, row_distance, max_x, max_y)
	line_indexes = get_line_indexes(start_indexes, improved_gradient, max_y, max_x)
	avg_pixel_values = get_line_values(line_indexes,img)
	peaks = get_line_locations(avg_pixel_values) #peaks contains the indices of the peak values 
	detected_lines = []
	for peak in peaks:
		detected_lines.append(line_indexes[peak])


	
	plot_line_detection(avg_pixel_values, peaks)
	plot_found_lines(img, detected_lines)

if __name__ == "__main__":
	main_run()
	plt.show()


