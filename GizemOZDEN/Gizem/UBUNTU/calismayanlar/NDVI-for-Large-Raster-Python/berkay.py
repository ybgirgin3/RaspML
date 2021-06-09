import os.path
from osgeo import gdal
from osgeo.gdalconst import *
import numpy as np

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-block', required=True)
    parser.add_argument('-redband', required=True)
    parser.add_argument('-NIRband', required=True)
    parser.add_argument('-i', required=True)
    parser.add_argument('-o', required=True)

    args = parser.parse_args()

    # sizes
    block_size = int(args.block)
    redband_num = int(args.redband)
    NIRband_num = int(args.NIRband)
    args = parser.parse_args()

    input_file = args.i
    output_file = args.o

    # get input file
    data = gdal.Open(input_file, GA_ReadOnly)
    x_size = data.RasterXSize
    y_size = data.RasterYSize
    nbands = data.RasterCount

    # read as gaster
    redband = data.GetRasterBand(redband_num)
    nirband = data.GetRasterBand(NIRband_num)

    # output parameters
    format_ = "GTiff"
    driver = gdal.GetDriverByName(format_)
    dst_data = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Float32)
    dst_data.SetGeoTransform(data.GetGeoTransform())
    dst_data.SetProjection(data.GetProjection())

    for i in range(0, y_size, block_size):

        rows = block_size if i + block_size < y_size else y_size - i

        for j in range(0, x_size, block_size):

            cols = block_size if j + block_size < x_size else x_size - j

            # extract block out of the whole raster
            red_arr = redband.ReadAsArray(j, i, cols, rows)
            nir_arr = nirband.ReadAsArray(j, i, cols, rows)

            # avoid zero situation
            nir_arr = nir_arr + 0.00001

            # calculate
            ndvi_arr = (nir_arr - red_arr) / (nir_arr + red_arr)
            dst_data.GetRasterBand(1).WriteArray(ndvi_arr, j, i)






