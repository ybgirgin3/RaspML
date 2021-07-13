import time
import numpy as np

import cv2
"""
import picamera
import picamera.array
"""


def label(image, text):
    """
    Labels the given image with the given text
    """
    return cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out



def runImage(img):
    frame = cv2.imread(img)

    W = 640
    H = 320

    #frame = cv2.resize(frame, (W,H), cv2.INTER_AREA)

    b,g,r = cv2.split(frame)

    # calculate 

    # bottom fraction
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01

    ndvi = (r.astype(float) - b) / bottom
    ndvi = contrast_stretch(ndvi)
    ndvi = ndvi.astype(np.uint8)

    # do the labelling
    label(b, "Blue")
    label(g, "Green")
    label(r, "NIR")
    label(ndvi, "NDVI")

    # combine ready for display
    combined = disp_multiple(b, g, r, ndvi)

    cv2.imshow('image', combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def runVideo(cap):
    # camerayı kullanmak için opencv kullan
    # resim karesi boyutu belirle
    W = 640
    H = 320
    while True:
        # use opencv instead
        success, frame = cap.read()
        if success:
            # print(type(frame)) # -> np.array

            # split image
            b, g, r = cv2.split(frame)

            # calculate 

            # bottom fraction
            bottom = (r.astype(float) + b.astype(float))
            bottom[bottom == 0] = 0.01

            ndvi = (r.astype(float) - b) / bottom
            ndvi = contrast_stretch(ndvi)
            ndvi = ndvi.astype(np.uint8)

            # do the labelling
            label(frame, "original")
            label(ndvi, "NDVI")

            cv2.imshow('ndvi image', ndvi)
            cv2.imshow('original image', frame)

            c = cv2.waitKey(7) % 0x100
            if c == 27:
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'V':
        cap = cv2.VideoCapture(0)
        runVideo(cap)
    elif sys.argv[1] == 'R':
        runImage(sys.argv[1])
