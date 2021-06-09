NDVI Test
==============

Calculating Normalized Differential Vegetation Index (NDVI) using numpy and scipy.
This was used more as a proof of concept in order to get some processing speed data.
Code is not yet optimized. Some flaws can be seen in the results, like glass and sky being falsely identified as plants. 

**Dataset:**

The original data set of NIR and RGB image pairs was downloaded from http://ivrgwww.epfl.ch/supplementary_material/cvpr11/ .
I renamed images and converted to jpg in order to reduce size. Modified files are in the DB folder.

**Results Sample:**
![RGB Image](/sample_rgb.jpg?raw=true)

![Greenly highlighted Plants](/sample_ndvi.jpg?raw=true)
