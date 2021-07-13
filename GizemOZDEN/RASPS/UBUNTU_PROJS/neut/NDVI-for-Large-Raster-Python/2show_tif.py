import rasterio as ras
from rasterio.plot import show


# single band
with ras.open(r'sample_ndvi.tif') as t:
    show(t)
