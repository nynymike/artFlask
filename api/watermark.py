from PIL import Image, ImageDraw, ImageFont
import os

def shrink(fn, size, newFN):
    im = Image.open(fn)
    im.thumbnail((size,size), Image.ANTIALIAS)
    im.save(newFN, 'PNG')

def create_copyright(text, fn, border=1):
    image = Image.new("RGBA", (222,25))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("HelveticaNeue-Light.ttf", 18)
    draw.text((10, 0), text, (88,88,88), font=font)
    bbox = image.getbbox()
    image = image.crop(bbox)
    (width, height) = image.size
    width += border * 2
    height += border * 2
    cropped_image = Image.new("RGBA", (width, height), (0,0,0,0))
    cropped_image.paste(image, (border, border))
    cropped_image.save(fn, 'PNG')

def watermark(original, watermark, fn):
    baseim = Image.open(original)
    logoim = Image.open(watermark)
    baseim.paste(logoim,(baseim.size[0]-logoim.size[0],baseim.size[1]-logoim.size[1]),logoim)
    baseim.save(fn, 'PNG')

def test():
    basedir = 'C:\\Users\\mike\\Documents\\GitHub\\artFlask\\upload\\'
    original_image = basedir + 'xdiart.jpeg'
    copyright_image = basedir + 'watermark.png'
    web_image = basedir + "web.png"
    new_image = basedir + 'final.png'
    shrink(original_image, 600, web_image)
    create_copyright("copyright Michael Schwartz", copyright_image)
    watermark(web_image, copyright_image, new_image)
    #os.remove(original_image)
    os.remove(copyright_image)
    os.remove(web_image)

if __name__ == '__main__':
    test()
