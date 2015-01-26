# -*- coding: utf-8 -*-

import StringIO
from PIL import Image


def scale_dimensions(width, height, longest_side):
    if width > longest_side:
        ratio = longest_side * 1. / width
        return (int(width * ratio), int(height * ratio))
    elif height > longest_side:
        ratio = longest_side * 1. / height
        return (int(width * ratio), int(height * ratio))
    return (width, height)


def resize_image(image, max_length, full_path=None):
    '''resize image longest side to max_length px, other side resize by scale
        full_path must contain full path to image and image name + extenshion
        if you need just image without saving it, don't pass full_path variable
        '''

    image = StringIO.StringIO(image.read())

    try:
        image = Image.open(image)
    except:
        return None

    (width, height) = image.size
    (width, height) = scale_dimensions(width, height, longest_side=160)
    image = image.convert('RGB')
    image = image.resize((width, height), Image.ANTIALIAS)
    image_file = StringIO.StringIO()
    if full_path:
        image.save(full_path, 'JPEG', quality=70)
        return image
    else:
        image.save(image_file, 'JPEG', quality=70)
        return image_file
