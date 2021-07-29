from skimage.transform import rotate
#from skimage.external.tifffile import imread, imsave
from skimage.io import imread, imsave
from skimage.draw import polygon
import numpy as np
import configparser
import sys, struct

# load image
# image = imread(fname=r'nir.tif')
# print(image[483][929])  # white
# print(image[480][930])  # white
#
# print(image[474][948])  # black
# print(image[815][910])  # black
# print()
# image = imread(fname=r'red.tif')
# print(image[483][929])  # white
# print(image[480][930])  # white
#
# print(image[474][948])  # black
# print(image[815][910])  # black
# print()
# image = imread(fname=r'rededge.tif')
# print(image[483][929])  # white
# print(image[480][930])  # white
#
# print(image[474][948])  # black
# print(image[815][910])  # black
# print()
# image = imread(fname=r'green.tif')
# print(image[483][929])  # white
# print(image[480][930])  # white
#
# print(image[474][948])  # black
# print(image[815][910])  # black

import osgeo.gdal as gdal
from take_photo import take
import cv2
import sys

#dataset = gdal.Open(r'indicies/red.tif', gdal.GA_ReadOnly)
#dataset = gdal.Open(r'indicies/RED_IMAGE.tif', gdal.GA_ReadOnly)
def main(f):
    dataset = gdal.Open(f, gdal.GA_ReadOnly)
    ysize = dataset.RasterYSize
    xsize = dataset.RasterXSize
    nbands = dataset.RasterCount
    print("""
    xsize: {}
    ysize: {}
    nbands: {}
    """.format(xsize, ysize, nbands))

    #print(dataset.GetProjection())
    band = dataset.GetRasterBand(1)
    print("xsize", band.XSize)
    scanline = band.ReadRaster(0, 948, band.XSize, 1, band.XSize, 1, gdal.GDT_Float32)
    #Unpack the line of data to be read as floating point data
    print(band.XSize, scanline)
    t = struct.unpack('f' * band.XSize, scanline)
    t = struct.unpack('H' * bytes([band.XSize, scanline]))
    #print(t)

    imsave('temp.tif', np.random.rand(3, 4, 301, 219))
    im = imread('temp.tif', key=0)
    print('temp.tiff', im.shape)


    #red = imread('temp.tif')
    #red = imread('indicies/RED_IMAGE.tif')
    red = imread(f)
    print("1", red.shape)
    #red = red[..., 0]
    #print("2",red.shape)
    #print(red[900, 900])
    #print("3",red)
    print(red.shape)
    imsave('template.jpg', red)

    redjpg = imread('template.jpg')
    print(redjpg.shape)

if __name__ == '__main__':
    if sys.argv[1] == 'R':
        main(r'indicies/RED_IMAGE.tif')
    elif sys.argv[1] == 'V':
        main(take(0))


