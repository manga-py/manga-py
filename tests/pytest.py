#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path, unlink
from sys import path as sys_path

from PIL import Image as PilImage

root_path = path.dirname(path.realpath(__file__))
sys_path.append(path.realpath(path.join(root_path, '..')))

from libs.image import Image


class TestCase(unittest.TestCase):
    paths = [
        ['/img1.jpg', '/temp/img1.jpg'],
        ['/img2.png', '/temp/img2.png'],
        ['/img3.jpg', '/temp/img3.jpg'],
        ['/img4.jpg', '/temp/img4.jpg'],
    ]

    def test_manual_crop(self):
        for file in self.paths:
            path.isfile(root_path + file[1]) and unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])

            img = Image(root_path + file[0])

            img.crop_manual((10, 0, image.size[0], image.size[1]), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])

            sizes = image.size
            cropped_sizes = cropped_image.size
            image.close()
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    # def test_auto_crop(self):
    #     file = self.paths[0]
    #     path.isfile(root_path + file[1]) and unlink(root_path + file[1])
    #
    #     image = PilImage.open(root_path + file[0])
    #
    #     img = Image(root_path + file[0])
    #
    #     img.crop_auto(root_path + file[1])
    #     img.close()
    #
    #     cropped_image = PilImage.open(root_path + file[1])
    #
    #     sizes = image.size
    #     cropped_sizes = cropped_image.size
    #     image.close()
    #     cropped_image.close()
    #
    #     self.assertTrue(sizes[0] < cropped_sizes[0])


if __name__ == '__main__':
    unittest.main()
