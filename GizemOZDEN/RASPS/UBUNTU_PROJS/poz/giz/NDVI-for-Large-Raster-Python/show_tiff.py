from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np

#ds = gdal.Open(r'sample.tif')

#inputRaster_path = r'sample.tif'
inputRaster_path = r'sample_ndvi.tif'

# _______________________________________________________________
# read input rows, cols, and bands of raster
ds = gdal.Open(inputRaster_path)
print(type(ds))
ysize = ds.RasterYSize
xsize = ds.RasterXSize
nbands = ds.RasterCount
print("""
xsize: {}
ysize: {}
nbands: {}
""".format(xsize, ysize, nbands))


print(ds.RasterCount)

# since there are 3 bands
# we store in 3 different variables
band1 = ds.GetRasterBand(1) # Red channel
band2 = ds.GetRasterBand(2) # Green channel
band3 = ds.GetRasterBand(3) # Blue channel


b1 = band1.ReadAsArray()
b2 = band2.ReadAsArray()
b3 = band3.ReadAsArray()


img = np.dstack((b1))
f = plt.figure()
plt.imshow(img)
plt.savefig('Tiff.png')
plt.show()

