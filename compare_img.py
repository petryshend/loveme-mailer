import wget, os, glob
from PIL import Image
from PIL import ImageChops

def img_equal(im1, im2):
    try:
        ImageChops.difference(im1, im2).getbbox()
    except Exception, e:
        return False
    return True

def hasPhoto(man_photo_url):
    default_img = Image.open('default.gif')
    downloaded_photo = wget.download(man_photo_url)
    man_photo = Image.open(downloaded_photo)
    return not img_equal(default_img, man_photo)

def removeJunkFiles():
    for file in glob.glob('*.jpg'):
        os.remove(file)
    for file in glob.glob('*.gif'):
        if file == 'default.gif':
            continue
        os.remove(file)
