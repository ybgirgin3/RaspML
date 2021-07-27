import rasterio as ras
from rasterio.plot import show
import sys


# single band
with ras.open(r'{}'.format(sys.argv[1])) as t:
    show(t)
