#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from PIL import Image
from helpers.remove_void.pexel import Pixel


class Cropper(Pixel):

    def __init__(self, file_path: str = None):
        if file_path:
            self.set_sourced_file(file_path)

    def _open_image(self, file_path: str):
        try:
            self.image = Image.open(file_path)
            if self.image.mode != 'RGB':  # fixed image mode
                self.image = self.image.convert('RGB')
            return self.image
        except OSError:
            return None

    def set_sourced_file(self, file_path):
        if not path.isfile(file_path):
            raise AttributeError('Error image path')
        self.original_image_path = file_path
        self.image = self._open_image(file_path)

    def set_epsilon(self, epsilon: int):
        self.epsilon = epsilon

    def __check_epsilon(self, side_sizes):
        width = self.image.size[0]
        height = self.image.size[1]

        side1 = side_sizes[0] <= self.epsilon >= side_sizes[1]
        side2 = width - side_sizes[2] <= self.epsilon >= height - side_sizes[3]

        if side1 and side2:
            return False
        return True

    def crop(self, sizes=None):
        if not isinstance(sizes, dict):
            raise AttributeError

        try:
            _sizes, _allow = self._prepare_crop_sizes(sizes)
            if _allow:
                img = Image.open(self.original_image_path)
                _sizes[2] = img.size[0] - _sizes[2]  # right
                _sizes[3] = img.size[1] - _sizes[3]  # bottom
                out_img = img.crop(_sizes)
                img.close()
                out_img.save(self.original_image_path)
                return True
        except (IOError, KeyError):
            pass
        return False

    def process(self, img_out_path, factor: int = 100, maximum_side_size: int = 30):

        if maximum_side_size < 1:
            return False

        ss = self._get_crop_sizes(factor, maximum_side_size)

        if not self.__check_epsilon(ss):
            return False

        try:
            image = self.image.crop(ss)
            image.save(img_out_path)
        except (IOError, KeyError):
            return False

        return True


class ImageFormat:

    @staticmethod
    def convert(file_path: str, format: str = 'png', quality: int = 95):
        """
        @ see http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
        :param file_path:
        :param format:
        :param quality:
        :return:
        """
        if not path.isfile(file_path):
            return False
        try:
            image = Image.open(file_path)
            if image.mode != 'RGB':  # fixed image mode
                image = image.convert('RGB')
            dest = '{}.{}'.format(file_path[:file_path.rfind('.')], format)
            image.save(dest, quality=quality)
            return dest
        except OSError:
            return False
