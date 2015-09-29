#! /usr/bin/env python

import argparse
import os
import math

from PIL import Image, ImageEnhance

"""
to run the script use :
python add_watermark.py --image small.jpg [--mark watermark.png]

if --mark argument is not specified, watermark.png is used by default from the DATA_DIR
"""

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'add_watermark_data')
DEFAULT_WATERMARK = Image.open(os.path.join(DATA_DIR, 'watermark.png'))
OPACITY = 0.5

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


def watermark(im, mark=DEFAULT_WATERMARK, opacity=OPACITY):
    """
    Adds a watermark to an image. im, mark arguments must be PIL image objects
    """
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    layer = Image.new('RGBA', im.size, (0,0,0,0))

    mark_ratio = float(mark.size[0]) / mark.size[1]
    min_dimension = min(im.size)
    if min_dimension < 400:
        scaling_factor = 0.45
    else:
        scaling_factor = 0.25

    if im.size[0] < im.size[1]:
        w = int(math.ceil(im.size[0] * scaling_factor))
        h = int(math.ceil(w / mark_ratio))
    else:
        h = int(math.ceil(im.size[1] * scaling_factor))
        w = int(math.ceil(h * mark_ratio))
    mark = mark.resize((w, h))
    layer.paste(mark, ((im.size[0] - w), (im.size[1] - h)))
    return Image.composite(layer, im, layer)

def main():
    parser = argparse.ArgumentParser(description='Watermark an image')
    parser.add_argument("--mark", '-m', help="the watermark image file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test", "-t", help="test this script", action="store_true")
    group.add_argument("--image", '-i', help="the image file that you wish to be watermarked")

    args = parser.parse_args()
    if args.mark:
        mark = Image.open(args.mark)
    else:
        mark = None

    if args.test:
        if mark is not None:
            run_test(mark)
        else:
            run_test()

    else:  # args.image
        im = Image.open(args.image)
        if mark is not None:
            marked_im = watermark(im, mark)
        else:
            marked_im = watermark(im)

        marked_im.save(str(os.path.splitext(args.image)[0]) + "_marked,png", "png")


def run_test(mark=DEFAULT_WATERMARK):
    small = Image.open(os.path.join(DATA_DIR, 'small.jpg'))
    large = Image.open(os.path.join(DATA_DIR, 'large.png'))

    watermark(small, mark).show()
    watermark(large, mark).show()

if __name__ == '__main__':
    main()