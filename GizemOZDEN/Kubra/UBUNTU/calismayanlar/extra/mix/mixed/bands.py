import rasterio
import os

#os.mkdir('3')
#os.mkdir('1')

for tif in os.listdir(os.getcwd()):
    if not os.path.isdir(tif) and not tif.endswith('.swp') and not tif.endswith('.py'):
        with rasterio.open(tif) as src:
            #print(src.profile['count'])
            if src.profile['count'] == 1:
                os.system(f"cp -r {tif} ../1_/")

            if src.profile['count'] == 3:
                os.system(f"cp -r {tif} ../3_/")

