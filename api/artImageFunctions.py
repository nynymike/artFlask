from PIL import Image, ImageDraw, ImageFont
import os
import httplib, urllib
from flask import current_app

def shrink(fn, size, newFN):
    im = Image.open(fn)
    im.thumbnail((size,size), Image.ANTIALIAS)
    im.save(newFN, 'PNG')

def create_copyright(text, fn, border=1):
    image = Image.new("RGBA", (222,25))
    draw = ImageDraw.Draw(image)
    print "%sHelveticaNeue-Light.ttf"%current_app.config['UPLOAD_FOLDER']
    font = ImageFont.truetype("%s/HelveticaNeue-Light.ttf"%current_app.config['UPLOAD_FOLDER'], 18)
    draw.text((10, 0), text, (219,180,124), font=font)
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

def genQRcode(url, fn):
    import qrcode
    ecc = qrcode.constants.ERROR_CORRECT_Q
    if len(url)<21: ecc = qrcode.constants.ERROR_CORRECT_H
    if len(url)>29: ecc = qrcode.constants.ERROR_CORRECT_M
    qr = qrcode.QRCode(
        version=2,
        error_correction=ecc,
        box_size=20,
        border=8,
        )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(fn, 'PNG')

def getShortURL(url):
    # Use http://linktrack.info  API
    params = urllib.urlencode({'login': 'bb063a6ed8952b2f246d85b53',
                               'pass': '7de896622639975',
                               'external_url': url})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPSConnection("linktrack.info")
    conn.request("POST", "/api/v1_0/makeLink", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def test(arg):
    basedir = 'C:\\Users\\mike\\Documents\\GitHub\\artFlask\\upload\\'
    if arg == 1:
        original_image = basedir + 'xdiart.jpeg'
        copyright_image = basedir + 'watermark.png'
        web_image = basedir + "web.png"
        new_image = basedir + 'final.png'
        tn = basedir + 'tn.png'
        shrink(original_image, 600, web_image)
        create_copyright("copyright Michael Schwartz", copyright_image)
        watermark(web_image, copyright_image, new_image)
        shrink(new_image, 100, tn)
        #os.remove(original_image)
        os.remove(copyright_image)
        os.remove(web_image)
    if arg == 2:
        testURL = 'https://www.eastaustinstudiotour.org/api/v1/f1d2c72a-b859-406e-aa52-6f4a06a66697/view'
        shortURL = getShortURL(testURL)
        print shortURL
        genQRcode(shortURL, basedir + "qrcode.png")

if __name__ == '__main__':
    test(2)
