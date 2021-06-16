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


dataset = gdal.Open(r'indicies/red.tif', gdal.GA_ReadOnly)
print(dataset.GetProjection())
band = dataset.GetRasterBand(1)
scanline = band.ReadRaster(0, 948, band.XSize, 1, band.XSize, 1, gdal.GDT_Float32)
#Unpack the line of data to be read as floating point data
t = struct.unpack('f' * band.XSize, scanline)
print(t)

imsave('temp.tif', np.random.rand(3, 4, 301, 219))
im = imread('temp.tif', key=0)
print(im.shape)


red = imread('red.tif')
red = red[..., 0]
print(red[900, 900])
print(red.shape)
imsave('template.jpg', red)

redjpg = imread('template.jpg')
print(redjpg.shape)
