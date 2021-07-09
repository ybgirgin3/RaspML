import os
import time
import glob
import sys
from skimage import data, io
from skimage import color
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np


# Lets set the directory to where we're saving the new images.
#os.chdir("NDVI")

# Load in all the NIR and RGB image file names
#nirImgs = glob.glob("..\\DB\\*_nir.jpg")
#nirImgs = glob.glob("../DB/*_nir.jpg")
#nirImgs = glob.glob("../../mix/*_nir.jpg")
#nirImgs = glob.glob("/home/berkay/code/freelance/RaspML/GizemOZDEN/Kubra/UBUNTU/calismayanlar/extra/mix/jpgs/*_nir.jpg")
nirImgs = glob.glob(f"{sys.argv[1]}/*_nir.jpg")
#rgbImgs = glob.glob("..\\DB\\*_rgb.jpg")
#rgbImgs = glob.glob("../../mix/*_rgb.jpg")
#rgbImgs = glob.glob("/home/berkay/code/freelance/RaspML/GizemOZDEN/Kubra/UBUNTU/calismayanlar/extra/mix/jpgs/*_rgb.jpg")
rgbImgs = glob.glob(f"{sys.argv[1]}/*_rgb.jpg")
# Used for tinting images green
greenMultiplier = [0, 1, 0]

start_time = time.time()

bad_image_counter = 0
good_image_counter = 0

def passImage(image):
    global shp
    if image == "nirImgs":
        shp = image.T.shape[1]

    else:
        shp = image.shape[1]

    if shp == 1024:
        return True
    else: return False

def NDVI(nir, rgb):
    # Calculate NDVI [(NIR - VIS) / (NIR + VIS)]
    if nir.shape[0] > rgb.shape[1]:
        ndvi = (nirImg[:, None] - rgbImg[None, :]) / (nirImg[:, None] + rgbImg[None, :])
    else:
        #ndvi = (rgbImg - nirImg) / (nirImg + rgbImg)
        ndvi = (nirImg[None, :] - rgbImg[:, None]) / (nirImg[None, :] + rgbImg[:, None])

    return ndvi


from tqdm import tqdm, trange
from colorama import Fore
for i in trange(0, len(nirImgs), bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)):
    # Load the next image pair from the set
    rgbImg = io.imread(str(rgbImgs[i]))
    nirImg = io.imread(str(nirImgs[i]))

    # control images
    if passImage(rgbImg) and passImage(nirImg):
        good_image_counter += 1

        # process get percentage
        # print image shapes
        rgbImg = rgbImg[:,:, 0].T
        nirImg = nirImg
        print("\r", end='')
        #print(f"process: {percent}", end = "", flush=True)

        #print("nirImg {} ".format(colored(nirImg.shape, "yellow")), end = "", flush=True)
        #print("rgbImg {}".format(colored(rgbImg.shape, "yellow")), end = "", flush=True)

        # calculate
        # matris sıkıntısı çözülürse eğer dahil et
        #ndvi = NDVI(nirImg, rgbImg)
        #print(ndvi)

    else: bad_image_counter += 1


    """
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
    """

# Print loop execution time
#print("--- %s seconds ---" % (time.time() - start_time))
print(colored(f"işlenebilecek resim sayısı: {good_image_counter}", "green"))
print(colored(f"işlenemez resim sayısı: {bad_image_counter}", "yellow"))

