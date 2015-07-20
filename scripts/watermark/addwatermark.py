from PIL import Image, ImageEnhance
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
    im = Image.open('./scripts/watermark/on.png')
    mark = Image.open('./scripts/watermark/off.png')
    print "here"
    #watermark(im, mark, 'tile', 0.5).show()
    watermark(im, mark, 'scale', 0.5).show()
    #watermark(im, mark, (100, 100), 0.5).show()
def run():
    print "lol"
    test()