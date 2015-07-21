import argparse
from PIL import Image, ImageEnhance

OPACITY = 0.5
"""
to run the script use :
python addwatermark.py -im on.png -mark off.png

"""


def reduce_opacity(im, opacity):
    """
    Returns an image with reduced opacity.
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """
    Adds a watermark to an image.
    """
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'scale':
        ratio = 0.24443
        w = int(im.size[0] * ratio)
        h = int(im.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) , (im.size[1] - h) ))
    else:
        layer.paste(mark, position)
    return Image.composite(layer, im, layer)

def test():
    parser = argparse.ArgumentParser()
    parser.add_argument("-im",help = "the image that you wish to add the watermark to" ,type =str,required=True)
    parser.add_argument("-mark",help = "the watermark image" ,type=str,required = True)
    parser.add_argument("-t",help="test images used!")

    args = parser.parse_args()
    if args.t:
        im = Image.open('on.png')
        im2 = Image.open('tot.png')
        im3 = Image.open('lol.jpg')

        mark = Image.open('off.png')
        print "here"
        watermark(im, mark, 'scale', OPACITY).show()
        watermark(im2, mark, 'scale', OPACITY).show()
        watermark(im3, mark, 'scale', OPACITY).show()
    else:
        im = Image.open(args.im)
        mark = Image.open(args.mark)
        watermark(im, mark, 'scale', OPACITY).show()

def run():
    test()
test()