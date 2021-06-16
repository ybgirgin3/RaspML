import os
from PIL import Image
import sys

#in_file = "land_shallow_topo_2048.tif"
in_file = sys.argv[1]

# ismi ayır
name, ext = os.path.splitext(in_file)

out_file = f"{name}.jpeg"

im = Image.open(in_file)
im.thumbnail(im.size)
im.save(out_file, "JPEG", quality=100)
