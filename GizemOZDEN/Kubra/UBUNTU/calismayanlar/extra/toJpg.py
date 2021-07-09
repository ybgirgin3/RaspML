from pprint import pprint
import sys
import os

#base_path = [i for i in os.listdir(".") if i != "jpgs" and not i.endswith("swp") and not i.endswith("py")]
#base_path = [os.path.abspath(i) for i in os.listdir(".") if os.path.isdir(i)]

# 
parentpath = sys.argv[1]
childs = [i for i in os.listdir(parentpath)]
#for child in os.listdir(parentpath):
#print(childs)
for i in childs:
    ret = os.listdir(i)
    print(ret)

