import os
import time
import glob
from skimage import data, io
from skimage import color
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np


# Lets set the directory to where we're saving the new images.
#os.chdir("NDVI")

# Load in all the NIR and RGB image file names
#nirImgs = glob.glob("..\\DB\\*_nir.jpg")
nirImgs = glob.glob("../DB/*_nir.jpg")
#rgbImgs = glob.glob("..\\DB\\*_rgb.jpg")
rgbImgs = glob.glob("../DB/*_rgb.jpg")
# Used for tinting images green
greenMultiplier = [0, 1, 0]

start_time = time.time()

for i in range(0, len(nirImgs)):
    # Load the next image pair from the set
    rgbImg = io.imread(str(rgbImgs[i]))
    nirImg = io.imread(str(nirImgs[i]))

    # Calculate NDVI [(NIR - VIS) / (NIR + VIS)]
    #print("hoop")
    new_c = [[0],[0]]
    nirImg = np.append(nirImg, new_c, axis=0)
    print("nirImg {}".format(colored(nirImg.T.shape, "yellow")))
    print("rgbImg {}".format(colored(rgbImg[:,:, 0].shape, "yellow")))


    ndviImg = (nirImg - rgbImg[:,:, 0].T) / (nirImg + rgbImg[:,:, 0].T)
    print("ndviImg: {}".format(colored(ndviImg, "red")))
    # Make sure values are thresholded.
    ndviImg[ndviImg > 1] = 1
    ndviImg[ndviImg < -1] = -1
    # Uncomment below to create images with green tint on healthy plants.
    #ndviImg = color.gray2rgb(ndviImg)
    #ndviImg[(ndviImg[:,:,1] > 0.35) & (ndviImg[:,:,1] < 0.85) ] *= greenMultiplier

    # Save the NDVI image
    io.imsave(str(i) + "_ndvi" + ".jpg", ndviImg)

# Print loop execution time
print("--- %s seconds ---" % (time.time() - start_time))
