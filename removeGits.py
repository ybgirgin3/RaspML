with open("git_files.txt", "r") as f:
    gits = f.readlines()


import os
for i in gits:
    os.system("rm -rf {}".format(i))
