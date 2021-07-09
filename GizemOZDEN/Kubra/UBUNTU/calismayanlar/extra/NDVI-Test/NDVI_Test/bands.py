import rasterio
import os

os.mkdir('../3_')
os.mkdir('../1_')

for tif in os.listdir(os.getcwd()):
    if not os.path.isdir(tif) and not tif.endswith('.swp') and not tif.endswith('.py') and not tif.endswith('.pyproj'):
        with rasterio.open(tif) as src:
            #print(src.profile['count'])
            if src.profile['count'] == 1:
                os.system(f"cp -r {tif} ../1_/")

            if src.profile['count'] == 3:
                os.system(f"cp -r {tif} ../3_/")

