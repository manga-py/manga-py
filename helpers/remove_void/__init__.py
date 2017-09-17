#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from os import path, rename, remove

_image = None
epsilon = 0


# I'm writing this crap because i can not think of anything better at this moment
def _test_pixel(max_s_s: int, factor: int, mode: int):

    width = _image.size[0]
    height = _image.size[1]
    not_height = height < max_s_s
    not_width = width < max_s_s

    if not_height or not_width:
        return 0

    pix = _image.load()

    def calculate_color(x, y):

        def calc_factor(col):
            _col = (col[0] + col[1] + col[2])
            return _col < ((255 + factor) // 2) * 3

        if calc_factor(pix[x, y]):
            if mode % 2:  # top, bottom
                if calc_factor(pix[x - 1, y]) or calc_factor(pix[x + 1, y]):
                    return True
            else:  # left, right
                if calc_factor(pix[x, y - 1]) or calc_factor(pix[x, y + 1]):
                    return True
        return False

    if mode == 0:  # left
        for width_iterator in range(max_s_s):
            if width_iterator < 1 or width_iterator > (max_s_s - 2):
                continue
            for height_iterator in range(height):
                xor = (width_iterator % 2) ^ (height_iterator % 2)
                if xor or (height_iterator < 1 or height_iterator > (height - 2)):
                    continue
                if calculate_color(width_iterator, height_iterator):
                    return width_iterator - 2

    elif mode == 1:  # top
        for height_iterator in range(max_s_s):
            if height_iterator < 1 or height_iterator > (max_s_s - 2):
                continue
            for width_iterator in range(width):
                xor = (width_iterator % 2) ^ (height_iterator % 2)
                if xor or width_iterator < 1 or width_iterator > (height - 2):
                    continue
                if calculate_color(width_iterator, height_iterator):
                    return height_iterator - 2

    elif mode == 2:  # right
        for width_iterator in range(max_s_s):
            if width_iterator < 1 or width_iterator > (max_s_s - 2):
                continue
            for height_iterator in range(height):
                xor = (width_iterator % 2) ^ (height_iterator % 2)
                if xor or height_iterator < 1 or height_iterator > (height - 2):
                    continue
                w = width - width_iterator - 1
                if calculate_color(w, height_iterator):
                    return w + 2

    elif mode == 3:  # bottom
        for height_iterator in range(max_s_s):
            if height_iterator < 1 or height_iterator > (max_s_s - 2):
                continue
            for width_iterator in range(width):
                xor = (width_iterator % 2) ^ (height_iterator % 2)
                if xor or width_iterator < 1 or width_iterator > (height - 2):
                    continue
                h = height - height_iterator - 1
                if calculate_color(width_iterator, h):
                    return h + 2

    else:
        raise ValueError('Error mode value')

    if mode < 2:
        return max_s_s
    if mode == 2:
        return width - max_s_s
    if mode == 3:
        return height - max_s_s


def _get_crop_sizes(factor: int, max_s_s: int):
    left = _test_pixel(max_s_s, factor, 0)
    top = _test_pixel(max_s_s, factor, 1)
    right = _test_pixel(max_s_s, factor, 2)
    bottom = _test_pixel(max_s_s, factor, 3)
    # add 1px white line
    left = left - 1 if left > 0 else 0
    top = top - 1 if top > 0 else 0
    right = right + 1 if right < _image.size[0] else right
    bottom = bottom + 1 if _image.size[1] < bottom > 0 else bottom
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


def prepare_crop_sizes(sizes):
    _sizes = [0, 0, 0, 0]  # (left, top, right, bottom)
    allow = False
    for n, i in enumerate(['left', 'top', 'right', 'bottom']):
        if sizes.get(i) and sizes.get(i) > 0:
            allow = True
            _sizes[n] = int(sizes[i])

    return _sizes, allow


def crop(img_path, sizes=None):
    if isinstance(sizes, dict) and path.isfile(img_path):
        try:
            _sizes, _allow = prepare_crop_sizes(sizes)
            if _allow:
                img = Image.open(img_path)
                _sizes[2] = img.size[0] - _sizes[2]  # right
                _sizes[3] = img.size[1] - _sizes[3]  # bottom
                out_img = img.crop(_sizes)
                img.close()
                out_img.save(img_path)
        except (IOError, KeyError):
            return False
        return True


def process(img_path, img_out_path, factor: int = 100, maximum_side_size: int = 30):
    if maximum_side_size < 1:
        return False

    if not _open_image(img_path):
        return False

    ss = _get_crop_sizes(factor, maximum_side_size)

    if ss[2] == 0 or ss[3] == 0:
        return False

    conditions = (ss[0], ss[1], _image.size[0] - ss[2], _image.size[1] - ss[3],)
    for i in conditions:
        if i < epsilon:
            return False

    try:
        image = _image.crop(ss)
        image.save(img_out_path)
    except (IOError, KeyError):
        return False
    return True


if __name__ == '__main__':
    print('Don\'t run this, please!')
