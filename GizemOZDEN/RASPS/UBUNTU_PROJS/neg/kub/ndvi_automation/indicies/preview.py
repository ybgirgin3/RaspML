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
jpg_name = cfg.get(para, 'jpg_name')
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

# transform matrix
angle_rad = angle_deg / 180 * np.pi
cos = np.cos(angle_rad)
sin = np.sin(angle_rad)
matrix = np.array(((cos, -sin), (sin, cos)))

redjpg = imread(jpg_name)
# draw
for i in range(rownum - 1, -1, -1):
    for j in range(rangenum):
        _x1 = j * net_x + x_offset
        _y1 = -(i * net_y + y_offset)
        _x2 = _x1 + plot_x
        _y2 = _y1 - plot_y
        x1, y1 = matrix.dot(np.array((_x1, _y1)))
        x2, y2 = matrix.dot(np.array((_x2, _y1)))
        x3, y3 = matrix.dot(np.array((_x2, _y2)))
        x4, y4 = matrix.dot(np.array((_x1, _y2)))
        r = np.array(tuple(map(lambda v: y - np.ceil(v), [y1, y2, y3, y4])))
        c = np.array(tuple(map(lambda v: x + np.ceil(v), [x1, x2, x3, x4])))
        rr, cc = polygon(r, c)
        redjpg[rr, cc] = (0, 0, 0)

imsave(output_name, redjpg)
