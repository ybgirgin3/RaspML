# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/12/16 16:57'

import os
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import *
import glob
import matplotlib.pyplot as plt
from take_photo import *

def pic(list_tif, out_path):
    print(list_tif)
    for tif in list_tif:
        in_ds = gdal.Open(tif, GA_ReadOnly)
        ysize = in_ds.RasterYSize
        xsize = in_ds.RasterXSize
        nbands = in_ds.RasterCount
        print("""
            xsize: {}
            ysize: {}
            nbands: {}
            """.format(xsize, ysize, nbands))

        # 获取文件所在路径以及不带后缀的文件名
        (filepath, fullname) = os.path.split(tif)
        (prename, suffix) = os.path.splitext(fullname)
        if in_ds is None:
            print('Could not open the file ' + tif)
        else:
            # 将MODIS原始数据类型转化为反射率
            red = in_ds.GetRasterBand(1).ReadAsArray()
            nir = in_ds.GetRasterBand(3).ReadAsArray()
            #ndvi = (nir - red) / (nir + red)
            # 将NAN转化为0值
            #nan_index = np.isnan(ndvi)
            #ndvi[nan_index] = 0
            #ndvi = ndvi.astype(np.float32)
            # 将计算好的NDVI保存为GeoTiff文件
            gtiff_driver = gdal.GetDriverByName('GTiff')
            # 批量处理需要注意文件名是变量，这里截取对应原始文件的不带后缀的文件名
            #out_ds = gtiff_driver.Create(out_path + prename + '_ndvi.tif', ndvi.shape[1], ndvi.shape[0], 1, gdal.GDT_Float32)
            out_ds = gtiff_driver.Create(out_path + prename + '_ndvi.tif', xsize, ysize, 1, gdal.GDT_Float32)
            # 将NDVI数据坐标投影设置为原始坐标投影
            out_ds.SetProjection(in_ds.GetProjection())
            out_ds.SetGeoTransform(in_ds.GetGeoTransform())
            ndvi = (nir - red) / (nir + red)
            out_band = out_ds.GetRasterBand(1).WriteArray(ndvi)

            plt.imshow(ndvi)  # 显示图片
            plt.axis('off')  # 不显示坐标轴
            plt.show()



if __name__ == '__main__':
    import sys

    list_tif = glob.glob('../data/*.tif')
    #out_path = 'D:/'
    out_path = '../'

    if sys.argv[1] == 'R':
        pic(list_tif, out_path)

    elif sys.argv[1] == 'V':
        l = []
        l.append(take())
        pic(l, out_path)




