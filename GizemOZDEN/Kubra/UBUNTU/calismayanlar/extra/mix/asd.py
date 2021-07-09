from pprint import pprint
import sys
import os

#base_path = [i for i in os.listdir(".") if i != "jpgs" and not i.endswith("swp") and not i.endswith("py")]
#base_path = [os.path.abspath(i) for i in os.listdir(".") if os.path.isdir(i)]

parentpath = sys.argv[1]
for childpath in os.listdir(parentpath):
    for file in os.listdir(childpath):
        pprint(file)






"""
import cv2, os
base_path = "mixed/"
new_path = "jpgs/"
for infile in os.listdir(base_path):
    print ("file : " + infile)
    read = cv2.imread(base_path + infile)
    outfile = infile.split('.')[0] + '.jpg'
    cv2.imwrite(new_path+outfile,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
"""


