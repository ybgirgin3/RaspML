from skimage.io import imread, imsave
from skimage.draw import polygon
import numpy as np
import configparser
import sys

# load configuration
cfg = configparser.ConfigParser()
cfg.read('config.cfg')
# cfg.read(sys.argv[1])

para = 'parameters'
red_name = cfg.get(para, 'red_name')
rededge_name = cfg.get(para, 'rededge_name')
nir_name = cfg.get(para, 'nir_name')
green_name = cfg.get(para, 'green_name')

jpg_name = cfg.get(para, 'jpg_name')

record_name = cfg.get(para, 'record_name')
output_name = cfg.get(para, 'output_name')

plot_x = cfg.getfloat(para, 'plot_x')
plot_y = cfg.getfloat(para, 'plot_y')
net_x = cfg.getfloat(para, 'net_x')
net_y = cfg.getfloat(para, 'net_y')

angle_deg = 360 - cfg.getfloat(para, 'angle_deg')

x_offset = cfg.getfloat(para, 'x_offset')
y_offset = cfg.getfloat(para, 'y_offset')

rownum = cfg.getint(para, 'rownum')
rangenum = cfg.getint(para, 'rangenum')
x = cfg.getint(para, 'x')
y = cfg.getint(para, 'y')

print('config read')

# load image
red = imread(red_name)
rededge = imread(rededge_name)
nir = imread(nir_name)
green = imread(green_name)

print('image read')

# transform matrix
angle_rad = angle_deg / 180 * np.pi
cos = np.cos(angle_rad)
sin = np.sin(angle_rad)
matrix = np.array(((cos, -sin), (sin, cos)))

'''
ndvi: calculate on every pixel, then average on pixels in a certain plot
ndre: calculate on every pixel
ccci: find max and min ndre among all pixels in all plots,
    then calculate ccci on every pixel,
    finally take an average ccci on pixels in a certain plot

drawing: ccci values scale to [0,255], colour ramp is black to red, black means high ccci
'''

# compute ndvi and ndre
ndvi_vals = []  # stores averaged ndvi for every plot
ndre_vals = []  # stores ndre for every plot and its pixels (2d array)
for i in range(rownum):
    for j in range(rangenum):
        _x1 = j * net_x + x_offset
        _y1 = -(i * net_y + y_offset)
        _x2 = _x1 + plot_x
        _y2 = _y1 - plot_y
        x1, y1 = matrix.dot((_x1, _y1))
        x2, y2 = matrix.dot((_x2, _y1))
        x3, y3 = matrix.dot((_x2, _y2))
        x4, y4 = matrix.dot((_x1, _y2))
        r = np.array(tuple(map(lambda v: y - np.ceil(v), (y1, y2, y3, y4))))
        c = np.array(tuple(map(lambda v: x + np.ceil(v), (x1, x2, x3, x4))))
        rr, cc = polygon(r, c)
        ndvi_plot = []
        ndre_plot = []
        for rrr, ccc in zip(rr, cc):  # for each pixel in one plot
            nir_val = nir[rrr, ccc][0].astype(float)
            red_val = red[rrr, ccc][0].astype(float)
            rededge_val = rededge[rrr, ccc][0].astype(float)
            ndvi = (nir_val - red_val) / (nir_val + red_val)
            ndvi_plot.append(ndvi)
            ndre = (nir_val - rededge_val) / (nir_val + rededge_val)
            ndre_plot.append(ndre)
        ndvi_vals.append(sum(ndvi_plot) / len(ndvi_plot))
        ndre_vals.append(ndre_plot)

print(sum(tuple(map(lambda v: len(v), ndre_vals))), 'pixels processed')

# ccci
ndre_flatten = [v for sublist in ndre_vals for v in sublist]
mmax = max(ndre_flatten)  # max among all pixels
mmin = min(ndre_flatten)
rrange = mmax - mmin
ccci_vals = []  # averaged ccci value for each plot
for sublist in ndre_vals:
    ccci_plot = tuple(map(lambda v: (v - mmin) / rrange, sublist))  # ccci values on pixels in one plot
    ccci_vals.append(sum(ccci_plot) / len(ccci_plot))

print('indices calculated')

# draw and record
redjpg = imread(jpg_name)
with open(record_name, 'w') as f:
    f.write('refid,row,range,ndvi,ccci\n')
    refid = 0
    ccci_max = max(ccci_vals)
    ccci_min = min(ccci_vals)
    ccci_range = ccci_max - ccci_min
    for i in range(rownum - 1, -1, -1):
        for j in range(rangenum):
            _x1 = j * net_x + x_offset
            _y1 = -(i * net_y + y_offset)
            _x2 = _x1 + plot_x
            _y2 = _y1 - plot_y
            x1, y1 = matrix.dot((_x1, _y1))
            x2, y2 = matrix.dot((_x2, _y1))
            x3, y3 = matrix.dot((_x2, _y2))
            x4, y4 = matrix.dot((_x1, _y2))
            r = np.array(tuple(map(lambda v: y - np.ceil(v), (y1, y2, y3, y4))))
            c = np.array(tuple(map(lambda v: x + np.ceil(v), (x1, x2, x3, x4))))
            rr, cc = polygon(r, c)
            ndvi_val = ndvi_vals[i * rangenum + j]
            ccci_val = ccci_vals[i * rangenum + j]
            # draw
            colour = np.ceil((ccci_max - ccci_val) / ccci_range * 255)
            redjpg[rr, cc] = (colour, 0, 0)
            # record
            entry = str(refid) + ',' \
                    + str(i + 1) + ',' \
                    + str(j + 1) + ',' \
                    + str(ndvi_val) + ',' \
                    + str(ccci_val) + '\n'
            f.write(entry)
            refid += 1

imsave(output_name, redjpg)
print('image and csv outputted')
