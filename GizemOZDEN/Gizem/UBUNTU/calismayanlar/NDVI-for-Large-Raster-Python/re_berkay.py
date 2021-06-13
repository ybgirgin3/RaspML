from osgeo import gdal
from osgeo.gdalconst import *

# open image
filen = 'land_shallow_topo_2048.tif'
#block = 500
#redband = 1
dataset = gdal.Open(filen, gdal.GA_ReadOnly)

# get sizes
x_size = dataset.RasterXSize
y_size = dataset.RasterYSize
n_bands = dataset.RasterCount

print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
                            dataset.GetDriver().LongName))

print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                    dataset.RasterYSize,
                                    dataset.RasterCount))

print("Projection is {}".format(dataset.GetProjection()))

geotransform = dataset.GetGeoTransform()

if geotransform:
    print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
    print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

"""
band = dataset.GetRasterBand(1)
print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
"""


min = band.GetMinimum()
max = band.GetMaximum()
if not min or not max:
    (min,max) = band.ComputeRasterMinMax(True)
print("Min={:.3f}, Max={:.3f}".format(min,max))

if band.GetRasterColorTable():
    print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))

scanline = band.ReadRaster(xoff=0, yoff=0,
                        xsize=band.XSize, ysize=1,
                        buf_xsize=band.XSize, buf_ysize=1,
                        buf_type=gdal.GDT_Float32)

fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
metadata = driver.GetMetadata()
if metadata.get(gdal.DCAP_CREATE) == "YES":
    print("Driver {} supports Create() method.".format(fileformat))

if metadata.get(gdal.DCAP_CREATECOPY) == "YES":
    print("Driver {} supports CreateCopy() method.".format(fileformat))

# işlemler
red_band = dataset.GetRasterBand(1)
nir_band = dataset.GetRasterBand(2)

drv = driver.Create(output_file, x_size, y_size, gdal.GDT_Byte)
drv.SetGeoTransform(dataset.GeoGeoTransform())
drv.SetProjection(dataset.GetProjection())

