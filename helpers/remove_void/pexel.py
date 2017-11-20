#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Pixel:

    original_image_path = None
    image = None
    epsilon = 2

    @staticmethod
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

    @staticmethod
    def __sides_helper(mode, out_iterator, in_iterator, side):
        iterator = out_iterator
        if mode > 1:
            iterator = side - iterator

        if mode % 2:  # top, bottom
            width, height = in_iterator, iterator
        else:
            width, height = iterator, in_iterator

        return iterator, width, height

    @staticmethod
    def _pixel_helper(mode, max_s_s, width, height):

        if mode < 2:
            return max_s_s
        if mode == 2:
            return width - max_s_s
        return height - max_s_s

    @staticmethod
    def _prepare_crop_sizes(sizes):
        _sizes = [0, 0, 0, 0]  # (left, top, right, bottom)
        allow = False
        for n, i in enumerate(['left', 'top', 'right', 'bottom']):
            if sizes.get(i) and sizes.get(i) > 0:
                allow = True
                _sizes[n] = int(sizes[i])

        return _sizes, allow

    @staticmethod
    def _get_sides(mode, width, height):
        if mode % 2:
            return width, height
        return height, width

    @staticmethod
    def _normalize_crop_sizes(left, top, right, bottom, sizes):

        left = left - 1 if left > 0 else 0
        top = top - 1 if top > 0 else 0
        right = right + 1 if right < sizes[0] else right
        bottom = bottom + 1 if sizes[1] < bottom > 0 else bottom

        return left, top, right, bottom

    def _calc_helper(self, factor, mode, max_s_s, width, height):

        pix = self.image.load()

        side1, side2 = self._get_sides(mode, width, height)

        for out_iterator in range(1, max_s_s - 2):
            for in_iterator in range(1, side1 - 2):

                # Chess table
                if (out_iterator % 2) ^ (in_iterator % 2):
                    continue

                iterator, width_iterator, height_iterator = self.__sides_helper(mode, out_iterator, in_iterator, side2)

                if self.__calculate_color(pix, factor, mode, width_iterator, height_iterator):
                    return iterator
        return 0

    def _get_crop_sizes(self, factor: int, max_s_s: int):
        left = self._pixel(max_s_s, factor, 0)
        top = self._pixel(max_s_s, factor, 1)
        right = self._pixel(max_s_s, factor, 2)
        bottom = self._pixel(max_s_s, factor, 3)
        # add 1px white line
        return self._normalize_crop_sizes(left, top, right, bottom, self.image.size)

    # I'm writing this crap because i can not think of anything better at this moment
    def _pixel(self, max_s_s: int, factor: int, mode: int):

        width = self.image.size[0]
        height = self.image.size[1]
        not_height = height < max_s_s
        not_width = width < max_s_s

        if not_height or not_width or abs(mode) > 3:
            return 0

        result = self._calc_helper(factor, mode, max_s_s, width, height)
        if result > 0:
            return result

        return self._pixel_helper(mode, max_s_s, width, height)
