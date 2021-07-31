import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
import glob
import os


# girdi dosyası
inpath = glob.glob("3_/*.tiff")
# çıktı dosyası
outpath  = "output/"

for tif in inpath:
    in_ds = gdal.Open(tif)
    (filepath, fullname) = os.path.split(tif)
    (prename, suffix) = os.path.splitext(fullname)

    if in_ds is None:
        print("could not open")
    else:
        red = in_ds.GetRasterBand(1).ReadAsArray() * 0.0001
        nir = in_ds.GetRasterBand(2).ReadAsArray() * 0.0001
        ndvi = (nir - red) / (nir + red)

        # get rid of nans
        nan_index = np.isnan(ndvi)
        ndvi[nan_index] = 0
        ndvi = ndvi.astype(np.float32)

        # driver
        gtiff = gdal.GetDriverByName('GTiff')

        out_ds = gtiff.Create(outpath + prename + "_ndvi.tif", ndvi.shape[1], ndvi.shape[0], 1, gdal.GDT_Float32)
        out_ds.SetProjection(in_ds.GetProjection())
        out_ds.SetGeoTransform(in_ds.GetGeoTransform())
        outband = out_ds.GetRasterBand(1)
        outband.WriteArray(ndvi)
        outband.FlushCache()

        plt.imshow(ndvi)
        plt.axis('off')
        plt.show()
