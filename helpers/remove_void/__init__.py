#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from os import path

_image = None
epsilon = 2


def __calculate_color(pix, factor, mode, offset_x, offset_y):
    def calc_factor(col):
        _col = (col[0] + col[1] + col[2])
        return _col < ((255 + factor) // 2) * 3

    if calc_factor(pix[offset_x, offset_y]):
        if mode % 2:  # top, bottom
            return calc_factor(pix[offset_x - 1, offset_y]) or calc_factor(pix[offset_x + 1, offset_y])
        # left, right
        return calc_factor(pix[offset_x, offset_y - 1]) or calc_factor(pix[offset_x, offset_y + 1])
    return False


def __sides_helper(mode, out_iterator, in_iterator, side):
    iterator = out_iterator
    if mode > 1:
        iterator = side - iterator

    if mode % 2:  # top, bottom
        width, height = in_iterator, iterator
    else:
        width, height = iterator, in_iterator

    return iterator, width, height


def __calc_helper(factor, mode, max_s_s, height, width):

    pix = _image.load()

    side1 = height if mode % 2 == 0 else width
    side2 = height if mode % 2 == 1 else width

    for out_iterator in range(1, max_s_s - 2):
        for in_iterator in range(1, side1 - 2):

            'Chess table'
            if (out_iterator % 2) ^ (in_iterator % 2):
                continue

            iterator, width_iterator, height_iterator = __sides_helper(mode, out_iterator, in_iterator, side2)

            if __calculate_color(pix, factor, mode, width_iterator, height_iterator):
                return iterator
    return 0


def __pixel(mode, max_s_s, width, height):

    if mode < 2:
        return max_s_s
    if mode == 2:
        return width - max_s_s
    return height - max_s_s


# I'm writing this crap because i can not think of anything better at this moment
def _pixel(max_s_s: int, factor: int, mode: int):

    width = _image.size[0]
    height = _image.size[1]
    not_height = height < max_s_s
    not_width = width < max_s_s

    if not_height or not_width:
        return 0

    if 0 <= mode < 4:
        result = __calc_helper(factor, mode, max_s_s, height, width)
        if result > 0:
            return result

    else:
        raise ValueError('Error mode value')

    return __pixel(mode, max_s_s, width, height)


def _get_crop_sizes(factor: int, max_s_s: int):
    left = _pixel(max_s_s, factor, 0)
    top = _pixel(max_s_s, factor, 1)
    right = _pixel(max_s_s, factor, 2)
    bottom = _pixel(max_s_s, factor, 3)
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


def __check_epsilon(side_sizes):
    width = _image.size[0]
    height = _image.size[1]

    side1 = side_sizes[0] <= epsilon >= side_sizes[1]
    side2 = width - side_sizes[2] <= epsilon >= height - side_sizes[3]

    if side1 and side2:
        return False

    return True


def process(img_path, img_out_path, factor: int = 100, maximum_side_size: int = 30):

    if maximum_side_size < 1:
        return False

    if not _open_image(img_path):
        return False

    ss = _get_crop_sizes(factor, maximum_side_size)

    if not __check_epsilon(ss):
        return False

    try:
        image = _image.crop(ss)
        image.save(img_out_path)
    except (IOError, KeyError):
        return False

    return True


if __name__ == '__main__':
    print('Don\'t run this, please!')
