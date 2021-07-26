# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/12/16 16:57'

import os
import numpy as np
from osgeo import gdal
import glob
import matplotlib.pyplot as plt


#list_tif = glob.glob('../data/*.tif')
out_path = '../'

def sub_main(in_ds, out_path):
    # 将MODIS原始数据类型转化为反射率
    red = in_ds.GetRasterBand(1).ReadAsArray() * 0.0001
    nir = in_ds.GetRasterBand(2).ReadAsArray() * 0.0001
    ndvi = (nir - red) / (nir + red)
    # 将NAN转化为0值
    nan_index = np.isnan(ndvi)
    ndvi[nan_index] = 0
    ndvi = ndvi.astype(np.float32)
    # 将计算好的NDVI保存为GeoTiff文件
    gtiff_driver = gdal.GetDriverByName('GTiff')
    # 批量处理需要注意文件名是变量，这里截取对应原始文件的不带后缀的文件名
    out_ds = gtiff_driver.Create(out_path + prename + '_ndvi.tif',
                     ndvi.shape[1], ndvi.shape[0], 1, gdal.GDT_Float32)
    # 将NDVI数据坐标投影设置为原始坐标投影
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(ndvi)
    out_band.FlushCache()

    plt.imshow(ndvi)  # 显示图片
    plt.axis('off')  # 不显示坐标轴
    plt.show()



# resim çek
def take_pic(vid):
    import cv2
    cap = cv2.VideoCapture(vid)
    while True:
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.imwrite('input_image.png', frame)
            cv2.destroyAllWindows()
            break

    cap.release()


def main(list_tif, out_path):
    if type(list_tif) == 'list':
        for tif in list_tif:
            in_ds = gdal.Open(tif)
            # 获取文件所在路径以及不带后缀的文件名
            (filepath, fullname) = os.path.split(tif)
            (prename, suffix) = os.path.splitext(fullname)
            if in_ds is None:
                print('Could not open the file ' + tif)
    elif type(list_tif) == 'str':
        in_ds = gdal.Open(list_tif)
        # 获取文件所在路径以及不带后缀的文件名
        (filepath, fullname) = os.path.split(tif)
        (prename, suffix) = os.path.splitext(fullname)
        if in_ds is None:
            print('Could not open the file ' + tif)


    sub_main(in_ds, out_path)



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 0:
        if sys.argv[1] == 'R':
            inp = glob.glob('../data/*.tif')
            outp = '../'
            main(inp, outp)

        elif sys.argv[1] == 'V':
            if sys.argv[2] == '0':
                vid = int(sys.argv[2])
            else: vid = str(sys.argv[2])

            take_pic(vid)
            main('input_image.png', outp)


