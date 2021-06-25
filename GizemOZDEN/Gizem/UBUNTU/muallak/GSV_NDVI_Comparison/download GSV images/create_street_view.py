import streetview as sw
from pprint import pprint

# fotolar 360 derece çekilmiş bir derece değeri girmek lazım
heading = 100

flat_dir = '.'

key = 'xZV6r2HKXujCd-OpFCcbMgVRVUY='
# { "lat": -26.705487625941643, "lng": 130.252984375 }
# 40.79406241617485, 30.40100914620992

#panoids = sw.panoids(lat=-33.85693857571269, lon=151.2144895142714)
panoids = sw.panoids(lat=40.79406241617485, lon=30.40100914620992)
pprint(panoids)
print(len(panoids))

if len(panoids) > 0:
    for pan in panoids:
        #sw.api_download(pan, heading, flat_dir, key)
        sw.api_download(pan, heading, flat_dir, key)


