
import numpy as np
import matplotlib.pyplot as plt
import scipy 
from scipy import fftpack
from scipy import interpolate
import sys

def get_fourier_values(img):

	FFTData = np.fft.fft2(img) #Here we find the Fourier Transform of the image
	FreqCompRows = np.fft.fftfreq(FFTData.shape[0]) #frequency in 1/pixels 
	FreqCompCols = np.fft.fftfreq(FFTData.shape[1])

	shiftrows = fftpack.fftshift( FreqCompRows ) # shift so that low spatial frequencies are in the center.
	shiftcols = fftpack.fftshift( FreqCompCols )

	return shiftrows, shiftcols

def get_shifted_fourier_chart(img):
	fourier = fftpack.fft2(img)
	fourier_shifted = fftpack.fftshift( fourier ) # shift so that low spatial frequencies are in the center.
	fourier_abs = np.abs(fourier_shifted) #This array that we use is the absolute value of the shifted fourier transform

	return fourier_shifted, fourier_abs

def get_row_values(fourier_abs, shiftrows, shiftcols):

	# Here we set the center point to 0 and then find the highest value (which should be the dot to the right)
	#find the index of the highest value point
	indices = np.unravel_index(np.argmax(fourier_abs, axis=None), fourier_abs.shape) 

	fourier_abs[indices[0]][indices[1]] = 0 #set the max value to 0 as this middle point is not useful (note that the index of this point is the middle of the 2D array)

	indices = np.unravel_index(np.argmax(fourier_abs, axis=None), fourier_abs.shape)

	row_frequency = shiftrows[indices[0]]
	column_frequency = shiftcols[indices[1]]

	frequency = np.sqrt(row_frequency*row_frequency + column_frequency*column_frequency)
	row_distance = 1/frequency

	row_angle = np.arctan(column_frequency/row_frequency)*(180/np.pi) #degrees of the row_angle 

	print("row_angle:")
	print(row_angle)

	gradient = np.tan(np.deg2rad(row_angle)) 
	
	return row_distance, row_angle


def plot_fourier(fourier_shifted, shiftrows, shiftcols):
	# These lines display the fourier plot
	plt.figure()
	plt.imshow(np.log(np.abs(fourier_shifted)), extent = (shiftcols[0], shiftcols[-1], shiftrows[0], shiftrows[-1]))
	plt.title('Fourier transform')


def plot_img(img, title):
	plt.figure()
	plt.imshow(img)
	plt.colorbar()
	plt.title(title)


def run_everything(img, plot):

	shiftrows, shiftcols = get_fourier_values(img)
	fourier_shifted, fourier_abs = get_shifted_fourier_chart(img)
	row_distance, row_angle = get_row_values(fourier_abs, shiftrows, shiftcols)
	if plot:
		plot_fourier(fourier_shifted, shiftrows, shiftcols)
		plt.show()

	return row_distance, row_angle


def main_run():
	# We want the images to be square and a power of 2 (256 x 256) or (512 x 512)
	img = plt.imread('../Media/cropped512/0.png').astype(float)
	shiftrows, shiftcols = get_fourier_values(img)
	fourier_shifted, fourier_abs = get_shifted_fourier_chart(img)
	row_distance, row_angle = get_row_values(fourier_abs, shiftrows, shiftcols)
	plot_fourier(fourier_shifted, shiftrows, shiftcols)
	plot_img(img, 'lines')


# ----- MAIN -----
if __name__ == "__main__":
	main_run()
	plt.show()


