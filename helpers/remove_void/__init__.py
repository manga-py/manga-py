#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import os
from PIL import Image, ImageDraw

_image = None


# I'm writing this crap because i can not think of anything better at this moment
def _test_pixel(max_s_s: int, factor: int, mode: int):
    width = _image.size[0] - 1
    height = _image.size[1] - 1
    if height < max_s_s or width < max_s_s:
        return 0
    pix = _image.load()
    if mode == 0:  # left
        print([range(max_s_s), range(height)])
        for j in range(max_s_s):
            for i in range(height):
                _ = pix[j, i]
                if _ == 0:
                    continue
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                print([S, (((255 + factor) // 2) * 3)])
                if S > (((255 + factor) // 2) * 3):
                    return j
    elif mode == 1:  # top
        for i in range(max_s_s):
            for j in range(width):
                _ = pix[j, i]
                if _ == 0:
                    continue
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                print([S, (((255 + factor) // 2) * 3)])
                if S > (((255 + factor) // 2) * 3):
                    return i
    if mode == 2:  # right
        for j in range(max_s_s):
            for i in range(height):
                _ = pix[width - j, i]
                if _ == 0:
                    continue
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                print([S, (((255 + factor) // 2) * 3)])
                if S > (((255 + factor) // 2) * 3):
                    return j
    elif mode == 3:  # bottom
        for i in range(max_s_s):
            for j in range(width):
                _ = pix[j, height - i]
                if _ == 0:
                    continue
                a = _[0]
                b = _[1]
                c = _[2]
                S = a + b + c
                print([S, (((255 + factor) // 2) * 3)])
                if S > (((255 + factor) // 2) * 3):
                    return i
    return 0


def _get_crop_sizes(factor: int, max_s_s: int):
    """
    :return: ImageDraw.Draw
    """
    left = _test_pixel(max_s_s, factor, 0)
    print(left)
    top = _test_pixel(max_s_s, factor, 1)
    print(top)
    right = _test_pixel(max_s_s, factor, 2)
    print(right)
    bottom = _test_pixel(max_s_s, factor, 3)
    print(bottom)
    return left, top, right, bottom


def _open_image(path: str):
    """
    :param path: absolute img path
    :return: bool
    """
    global _image
    try:
        _image = Image.open(path)
    except OSError:
        return False
    return True



def process(img_path, img_out_path, factor: int = 100, maximum_side_size: int = 30):
    if not _open_image(img_path):
        return False
    _ = _image.load()
    sizes = _get_crop_sizes(factor, maximum_side_size)
    # Image.crop( (left, upper, right, lower, ) )
    # print(sizes)
    exit()
    if sizes[2] == 0 or sizes[1] == 0:
        return False
    image = _image.crop(sizes)
    # print(image)
    # exit()
    image.save(img_out_path)
    return True


print(process('./7ce65ff9daf3512829763b91cb41ef37.jpg', './img2.png'))


if __name__ == '__main__':
    print('Don\'t run this, please!')
