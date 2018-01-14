#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path, unlink, makedirs
from sys import path as sys_path

from PIL import Image as PilImage

root_path = path.dirname(path.realpath(__file__))
sys_path.append(path.realpath(path.join(root_path, '..')))

from libs.providers import get_provider
from libs.providers.provider import Provider
from libs.image import Image


class TestCase(unittest.TestCase):
    paths = [
        ['/img1.jpg', '/temp/img1.jpg'],
        ['/img2.png', '/temp/img2.png'],
        ['/img3.jpg', '/temp/img3.jpg'],
        ['/img4.jpg', '/temp/img4.jpg'],
        ['/img5.png', '/temp/img5.png'],
        ['/img6.gif', '/temp/img6.gif'],
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

    def test_manual_crop_with_offsets(self):
        for file in self.paths:
            path.isfile(root_path + file[1]) and unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])

            img = Image(root_path + file[0])

            img.crop_manual_with_offsets((10, 0, 0, 0), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])

            sizes = image.size
            cropped_sizes = cropped_image.size
            image.close()
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    def test_auto_crop1(self):
        file = self.paths[0]
        path.isfile(root_path + file[1]) and unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])

        img = Image(root_path + file[0])

        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])

        sizes = image.size
        cropped_sizes = cropped_image.size
        image.close()
        cropped_image.close()

        self.assertTrue(sizes[0] > cropped_sizes[0])

    def test_auto_crop2(self):
        file = self.paths[1]
        path.isfile(root_path + file[1]) and unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])

        img = Image(root_path + file[0])

        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])

        sizes = image.size
        cropped_sizes = cropped_image.size
        image.close()
        cropped_image.close()

        self.assertTrue(sizes[0] == cropped_sizes[0])

    def test_auto_crop3(self):
        file = self.paths[4]
        path.isfile(root_path + file[1]) and unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])

        img = Image(root_path + file[0])

        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])

        sizes = image.size
        cropped_sizes = cropped_image.size
        image.close()
        cropped_image.close()

        self.assertTrue(sizes[0] == (2 + cropped_sizes[0]))  # 2px black line

    def test_image_not_found(self):
        self.assertRaises(AttributeError, lambda: Image(root_path))

    def test_gray1(self):
        file = self.paths[1]
        path.isfile(root_path + file[1]) and unlink(root_path + file[1])
        image = Image(root_path + file[0])

        image.gray(root_path + file[1])
        image.close()

        image = PilImage.open(root_path + file[1])
        index = image.mode.find('L')
        image.close()

        self.assertTrue(index == 0)

    def test_convert(self):
        file = self.paths[0][0]
        image = Image(root_path + file)

        basename = file[0:file.find('.')]
        basename = root_path + '/temp' + basename + '.bmp'
        image.convert(basename)
        image.close()

        self.assertTrue(path.isfile(basename))

    # success
    def test_get_provider1(self):
        provider = get_provider('http://readmanga.me/manga/name/here')
        self.assertIsInstance(provider(), Provider)

    # failed
    def test_get_provider2(self):
        provider = get_provider('http://google.com/manga/name/here')
        self.assertFalse(provider)

    def test_(self):
        pass


if __name__ == '__main__':
    path.isdir(root_path + '/temp') or makedirs(root_path + '/temp')
    unittest.main()
