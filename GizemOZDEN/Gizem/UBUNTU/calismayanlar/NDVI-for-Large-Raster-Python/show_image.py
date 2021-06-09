import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

def show_image(dataFile, arr1, arr2):
    dat = gdal.Open(r'{}'.format(dataFile))
    print(f"dat.RasterCount {dat.RasterCount}") #-> 1

    # stacking image
    img = np.stack((arr1,arr2))
    f = plt.figure()
    #plt.imshow(img)
    plt.savefig(f"{dataFile}.png")
    plt.show()
