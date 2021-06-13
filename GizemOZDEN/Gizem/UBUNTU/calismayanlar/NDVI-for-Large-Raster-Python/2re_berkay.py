import numpy as np
import cv2

def ndvi(frame):
    lower_lim = 5

    H, W = frame[:,:,0].shape
    # create blank image
    ndvi_img = np.zeros((H, W, 3), np.uint8)
    ndvi = np.zeros((H, W), np.uint8)
    red  = np.zeros((H, W), np.uint8)
    blue = np.zeros((H, W), np.uint8)

    # now get the specific channels: B,G,R
    red  = (frame[:,:,2].astype('float'))
    blue = (frame[:,:,0].astype('float'))

    # perform ndvi calculation
    summ = red + blue
    summ[summ < lower_lim] = lower_lim

    redChannel  = (ndvi - 128) * 2
    blueChannel = ((255 - ndvi) * 2)
    redChannel[ndvi < 128] = 0
    blueChannel[ndvi >= 128] = 0

    ndvi_img[:,:,2] = redChannel
    ndvi_img[:,:,0] = blueChannel
    ndvi_img[:,:,1] = 255 - (blueChannel + redChannel)

    return ndvi_img


src = cv2.imread("land_shallow_topo_2048.jpeg")
ndvi_image = ndvi(src)
#print(ndvi_image)

