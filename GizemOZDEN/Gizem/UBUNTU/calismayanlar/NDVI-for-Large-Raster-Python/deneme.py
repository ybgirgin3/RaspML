import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import sys

#dataset = gdal.Open(r'land_shallow_topo_2048.tif')
dataset = gdal.Open(r'{sys.argv[1]}')
print(dataset.RasterCount)
# since there are 3 bands
# we store in 3 different variables
band1 = dataset.GetRasterBand(1) # Red channel
band2 = dataset.GetRasterBand(2) # Green channel
band3 = dataset.GetRasterBand(3) # Blue channel
b1 = band1.ReadAsArray()
b2 = band2.ReadAsArray()
b3 = band3.ReadAsArray()
img = np.dstack((b1, b2, b3))
f = plt.figure()
plt.imshow(img)
plt.savefig('Tiff.png')
plt.show()

