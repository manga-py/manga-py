#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image

_image = None


# I'm writing this crap because i can not think of anything better at this moment
def _test_pixel(max_s_s: int, factor: int, mode: int):
    width = _image.size[0]
    height = _image.size[1]
    if height < max_s_s or width < max_s_s:
        return 0
    pix = _image.load()
    if mode == 0:  # left
        for j in range(max_s_s):
            for i in range(height):
                _ = pix[j, i]
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                if S < (((255 + factor) // 2) * 3):
                    return j
    elif mode == 1:  # top
        for i in range(max_s_s):
            for j in range(width):
                _ = pix[j, i]
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                if S < (((255 + factor) // 2) * 3):
                    return i

    elif mode == 2:  # right
        for j in range(max_s_s):
            for i in range(height):
                w = width - j - 1
                _ = pix[w, i]
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                if S < (((255 + factor) // 2) * 3):
                    return w

    elif mode == 3:  # bottom
        for i in range(max_s_s):
            for j in range(width):
                h = height - i - 1
                _ = pix[j, h]
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                if S < (((255 + factor) // 2) * 3):
                    return h

    else:
        raise ValueError('Error mode value')

    if mode < 2:
        return max_s_s
    if mode == 2:
        return width - max_s_s - 1
    if mode == 3:
        return height - max_s_s - 1


def _get_crop_sizes(factor: int, max_s_s: int):
    left = _test_pixel(max_s_s, factor, 0)
    top = _test_pixel(max_s_s, factor, 1)
    right = _test_pixel(max_s_s, factor, 2)
    bottom = _test_pixel(max_s_s, factor, 3)
    # add 1px white line
    left = left - 1 if left > 0 else left
    top = top - 1 if top > 0 else top
    right = right + 1 if right < _image.size[0] - 1 else right
    bottom = bottom - 1 if bottom < _image.size[1] - 1 else bottom
    return left, top, right, bottom


def _open_image(path: str):
    global _image
    try:
        _image = Image.open(path)
        if _image.mode != 'RGB':  # fixed image mode
            _image = _image.convert('RGB')
    except OSError:
        return False
    return True


def process(img_path, img_out_path, factor: int = 100, maximum_side_size: int = 30):
    if not _open_image(img_path):
        return False
    _ = _image.load()
    ss = _get_crop_sizes(factor, maximum_side_size)
    if ss[2] == 0 or ss[3] == 0:
        return False
    if ss[0] == 0 and ss[1] == 0 and ss[2] == _image.size[0] and ss[3] == _image.size[1]:
        # original size
        return False
    try:
        image = _image.crop(ss)
        image.save(img_out_path)
    except (IOError, KeyError):
        return False
    return True


if __name__ == '__main__':
    print('Don\'t run this, please!')
