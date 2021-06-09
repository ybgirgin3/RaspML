from skimage.io import imread, imsave
from skimage.color import grey2rgb
import numpy as np
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')
# cfg.read(sys.argv[1])
para = 'parameters'
red_name = cfg.get(para, 'red_name')
jpg_name = cfg.get(para, 'jpg_name')

red = imread(red_name)
red = red[..., 0]  # select only the grey scale channel
grey_max = red.max()
for i in range(red.shape[0]):
    for j in range(red.shape[1]):
        red[i, j] = np.ceil(red[i, j] / grey_max * 255)

red = grey2rgb(red)
imsave(jpg_name, red)
