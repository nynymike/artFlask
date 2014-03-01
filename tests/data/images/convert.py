from PIL import Image
import os

files = os.listdir(".")
for file in files:
    baseFN, ext = file.split(".")
    if ext.lower()=="jpg":
        image=Image.open(file)
        image.save("%s.png" % baseFN, "PNG")
        print "converted %s to %s.png" % (file, baseFN)
