#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import math
import operator
import unittest
from functools import reduce
from os import path

from PIL import Image as PilImage, ImageChops

from manga_py.crypt import sunday_webry_com
from manga_py.crypt.puzzle import Puzzle
from manga_py.crypt import mangago_me
from manga_py.crypt import viz_com

root_path = path.dirname(path.realpath(__file__))


class TestMatrix(unittest.TestCase):
    @staticmethod
    def _rmsdiff(im1, im2):
        """Calculate the root-mean-square difference between two images"""
        h = ImageChops.difference(im1, im2).histogram()
        # calculate rms
        return math.sqrt(
            reduce(
                operator.add,
                map(lambda h, i: h * (i ** 2), h, range(256))
            ) / (float(im1.size[0]) * im1.size[1])
        )

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

    def test_solve_mangago(self):
        urls = [
            (
                'mangago1_orig.jpeg',
                'mangago1_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418858/962c5915bbe6f4ab0903149b5d94baba796a5cf059389458858fdeb74ddc02a4.jpeg'
            ),
            (
                'mangago2_orig.jpeg',
                'mangago2_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418858/53e50ae9291f4ab0903149b5d94baba796a5cf059383846d7d1f4dc72e9f75f9.jpeg'
            ),
            (
                'mangago3_orig.jpeg',
                'mangago3_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418859/c56e8e1f5baf770212313f5e9532ec5e6103b61e956e06496929048f98e33004.jpeg'
            ),
            (
                'mangago4_orig.jpeg',
                'mangago4_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418859/5af9065f5b2e2169a4bfd805e9aa21d3112d498d68c6caa9046af4b06a723170.jpeg'
            ),
            (
                'mangago5_orig.jpeg',
                'mangago5_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418859/34f05a15df5ae2169a4bfd805e9aa21d3112d498d68c765523c20c307fa0fda2.jpeg'
            ),
            (
                'mangago6_orig.jpeg',
                'mangago6_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/make_me_bark/418864/0d76361a3cf5baf770212313f5e9532ec5e6103b616618337cb81b6acf9c1912.jpeg'
            ),
            (
                'mangago7_orig.jpeg',
                'mangago7_reference.jpeg',
                'http://iweb7.mangapicgallery.com/r/cspiclink/lookism/443703/dbdf873a11bafad56c41ff7fbed622aa76e19f3564e5d52a6688d6d9e3c57fb2.jpeg'
            ),
        ]

        for i in urls:
            img = path.join(root_path, 'mosaic', i[0])
            dst = path.join(root_path, 'temp', i[0])

            ref = path.join(root_path, 'mosaic', i[1])

            mangago_me.MangaGoMe.puzzle(img, dst, i[2])

            # compare
            src = PilImage.open(ref)
            ref = PilImage.open(dst)
            deviation = self._rmsdiff(src, ref)
            src.close()
            ref.close()
            self.assertTrue(deviation < 10)

    def test_solve_viz_com(self):
        deviations = []
        for i in range(7):
            src_path = root_path + '/mosaic/viz/index{}.jfif'.format(i)
            ref_path = root_path + '/temp/canvas{}.png'.format(i)
            solved_path = root_path + '/mosaic/viz/canvas{}.png'.format(i)
            ref = viz_com.solve(src_path, {'width': 800, 'height': 1200})
            ref.save(ref_path)
            solved = PilImage.open(solved_path)
            deviation = self._rmsdiff(solved, ref)
            solved.close()
            print(f"Deviation: {deviation}")

            deviations.append(deviation < 10)

        self.assertTrue(all(deviations))
