#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image

_image = None
epsilon = 0


# I'm writing this crap because i can not think of anything better at this moment
def _test_pixel(max_s_s: int, factor: int, mode: int):

    width = _image.size[0]
    height = _image.size[1]
    if height < max_s_s or width < max_s_s:
        return 0

    def calculate_color(color_mask):
        color_sum = (color_mask[0] + color_mask[1] + color_mask[2])
        return color_sum < ((255 + factor) // 2) * 3

    pix = _image.load()

    if mode == 0:  # left
        for width_iterator in range(max_s_s):
            for height_iterator in range(height):
                if calculate_color(pix[width_iterator, height_iterator]):
                    return width_iterator

    elif mode == 1:  # top
        for height_iterator in range(max_s_s):
            for width_iterator in range(width):
                if calculate_color(pix[width_iterator, height_iterator]):
                    return height_iterator

    elif mode == 2:  # right
        for width_iterator in range(max_s_s):
            for height_iterator in range(height):
                w = width - width_iterator - 1
                if calculate_color(pix[w, height_iterator]):
                    return w

    elif mode == 3:  # bottom
        for height_iterator in range(max_s_s):
            for width_iterator in range(width):
                h = height - height_iterator - 1
                if calculate_color(pix[width_iterator, h]):
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
    if ss[0] <= epsilon\
            and ss[1] <= epsilon\
            and _image.size[0] - ss[2] <= epsilon\
            and _image.size[1] - ss[3] <= epsilon:
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
