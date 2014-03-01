from PIL import Image
import os

files = os.listdir(".")
for file in files:
    print file
    baseFN, ext = file.split(".")
    if ext.lower()=="jpg":
        image=Image.open(file)
        image.save("%s.png" % baseFN, "PNG")
