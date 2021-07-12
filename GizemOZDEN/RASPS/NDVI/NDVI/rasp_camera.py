import getopt
import sys

import cv2
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap


class NDVI(object):
    def __init__(self, file_path, output_file=False, colors=False):
        #self.image = plt.imread(file_path)
        self.image = cv2.imread(file_path)
        self.output_name = output_file or 'NDVI.jpg'
        self.colors = colors or ['gray', 'gray', 'red', 'yellow', 'green']

    def create_colormap(self, *args):
        return LinearSegmentedColormap.from_list(name='custom1', colors=args)

    def create_colorbar(self, fig, image):
        position = fig.add_axes([0.125, 0.19, 0.2, 0.05])
        norm = colors.Normalize(vmin=-1., vmax=1.)
        cbar = plt.colorbar(image,
                            cax=position,
                            orientation='horizontal',
                            norm=norm)
        cbar.ax.tick_params(labelsize=6)
        tick_locator = ticker.MaxNLocator(nbins=3)
        cbar.locator = tick_locator
        cbar.update_ticks()
        cbar.set_label("NDVI", fontsize=10, x=0.5, y=0.5, labelpad=-25)

    def convert(self):
        """
        This function performs the NDVI calculation and returns an GrayScaled frame with mapped colors)
        """
        NIR = (self.image[:, :, 0]).astype('float')
        blue = (self.image[:, :, 2]).astype('float')
        green = (self.image[:, :, 1]).astype('float')
        bottom = (blue - green) ** 2
        bottom[bottom == 0] = 1  # remove 0 from nd.array
        VIS = (blue + green) ** 2 / bottom
        NDVI = (NIR - VIS) / (NIR + VIS)

        fig, ax = plt.subplots()
        image = ax.imshow(NDVI, cmap=self.create_colormap(*self.colors))
        plt.axis('off')

        #self.create_colorbar(fig, image)

        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(self.output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)
        # plt.show()


    def convertVid(self):
        NIR = (self.image[:, :, 0]).astype('float')
        blue = (self.image[:, :, 2]).astype('float')
        green = (self.image[:, :, 1]).astype('float')
        bottom = (blue - green) ** 2
        bottom[bottom == 0] = 1  # remove 0 from nd.array
        VIS = (blue + green) ** 2 / bottom
        NDVI = (NIR - VIS) / (NIR + VIS)

        #extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        #fig.savefig(self.output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)
        cv2.imshow('green', green)



def runVideo(cap):
    while True:
        s, frame = cap.read()
        if s:
            blue_ndvi = NDVI(frame, output_file=output_file or False, colors=colors or False)
            blue_ndvi.convertVid()

            key = cv2.waitKey(7) % 0x100
            if key == 27:
                break

def main(argv, T=None):
    try:
        opts, args = getopt.getopt(argv, "i:o:c", ["input_file=", "output_file=", "colors"])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    input_file = dict(opts).get('-i')
    output_file = dict(opts).get('-o')
    if '-c' in dict(opts).keys() and args:
        colors = args
    elif '-c' not in dict(opts).keys() and args:
        print('please add "-c" in order to add custom colors for image color map')
    else:
        colors = False

    if T == 'R':
        blue_ndvi = NDVI(input_file, output_file=output_file or False, colors=colors or False)
        blue_ndvi.convert()
    if T == 'V':
        cap = cv2.VideoCapture(input_file)
        runVideo(cap)
       
if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[1])
