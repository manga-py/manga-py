#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import math
import operator
import unittest
from functools import reduce
from os import path

from PIL import Image as PilImage, ImageChops

from manga_py.crypt.puzzle import Puzzle
from manga_py.crypt import sunday_webry_com

root_path = path.dirname(path.realpath(__file__))


class TestMatrix(unittest.TestCase):
    @staticmethod
    def _rmsdiff(im1, im2):
        """Calculate the root-mean-square difference between two images"""
        h = ImageChops.difference(im1, im2).histogram()
        # calculate rms
        return math.sqrt(reduce(operator.add, map(lambda h, i: h * (i ** 2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

    def test_jpg(self):
        file_src = root_path + '/mosaic/tonarinoyj_jp_orig.jpg'  # tonarinoyj.jp  image
        file_ref = root_path + '/mosaic/tonarinoyj_jp_reference.jpg'
        file_dst = root_path + '/temp/tonarinoyj_jp_mosaic.jpg'

        div_num = 4
        matrix = {}
        for i in range(div_num * div_num):
            matrix[i] = (i % div_num) * div_num + int(i / div_num)
        p = Puzzle(div_num, div_num, matrix, 8)
        p.need_copy_orig = True
        p.de_scramble(file_src, file_dst)

        src = PilImage.open(file_dst)
        ref = PilImage.open(file_ref)

        deviation = self._rmsdiff(src, ref)
        src.close()
        ref.close()
        self.assertTrue(deviation < 10)

    def test_png(self):
        file_src = root_path + '/mosaic/tonarinoyj_jp_orig.png'  # tonarinoyj.jp  image
        file_ref = root_path + '/mosaic/tonarinoyj_jp_reference.png'
        file_dst = root_path + '/temp/tonarinoyj_jp_mosaic.png'

        div_num = 4
        matrix = {}
        for i in range(div_num * div_num):
            matrix[i] = (i % div_num) * div_num + int(i / div_num)
        p = Puzzle(div_num, div_num, matrix, 8)
        p.need_copy_orig = True
        p.de_scramble(file_src, file_dst)

        src = PilImage.open(file_dst)
        ref = PilImage.open(file_ref)

        deviation = self._rmsdiff(src, ref)
        src.close()
        ref.close()
        self.assertTrue(deviation < 10)

    def test_sunday_webry_com(self):
        decoder = sunday_webry_com.SundayWebryCom()

        with open(root_path + '/mosaic/sunday_reference_matrix.json') as f:
            result = json.loads(f.read())

        n = 0
        for _i, _r in enumerate(result):

            result_py = decoder.solve(848, 1200, 64, 64, _i + 1)

            for i, r in enumerate(_r):
                p = result_py[i]
                if (
                    r['srcX'] != p['srcX'] or
                    r['srcY'] != p['srcY'] or
                    r['destX'] != p['destX'] or
                    r['destY'] != p['destY'] or
                    r['width'] != p['width'] or
                    r['height'] != p['height']
                ):
                    n += 1

        self.assertTrue(n < 1)

    def test_solve_sunday_webry_com(self):
        decoder = sunday_webry_com.SundayWebryCom()
        puzzle = sunday_webry_com.MatrixSunday()

        src = root_path + '/mosaic/sunday_orig.jpg'
        file_dst = root_path + '/temp/sunday_mosaic2.jpg'
        file_ref = root_path + '/mosaic/sunday_reference.jpg'

        result_py2 = decoder.solve_by_img(src, 64, 64, 2)

        puzzle.de_scramble(src, file_dst, result_py2)

        src = PilImage.open(file_dst)
        ref = PilImage.open(file_ref)

        deviation = self._rmsdiff(src, ref)

        self.assertTrue(deviation < 10)

    def test_solve_plus_comico_js(self):
        src = root_path + '/mosaic/plus_comico_jp_orig.jpg'
        file_dst = root_path + '/temp/plus_comico_jp_mosaic.jpg'
        file_ref = root_path + '/mosaic/plus_comico_jp_reference.jpg'

        _matrix = '3,14,5,8,10,12,4,2,1,6,15,13,7,11,0,9'.split(',')

        div_num = 4
        matrix = {}
        n = 0
        for i in _matrix:
            matrix[int(i)] = n
            n += 1

        p = Puzzle(div_num, div_num, matrix, 8)
        p.need_copy_orig = True
        p.de_scramble(src, file_dst)

        src = PilImage.open(file_dst)
        ref = PilImage.open(file_ref)

        deviation = self._rmsdiff(src, ref)
        src.close()
        ref.close()
        self.assertTrue(deviation < 10)
