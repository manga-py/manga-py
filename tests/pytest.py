#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import math
import operator
import unittest
from functools import reduce
from os import path
from shutil import copyfile
from sys import path as sys_path

from PIL import Image as PilImage, ImageChops
from pyvirtualdisplay import Display

root_path = path.dirname(path.realpath(__file__))
sys_path.append(path.realpath(path.join(root_path, '..')))

from src.providers import get_provider
from src.base_classes import Base, Archive, Static
from src.provider import Provider
from src.image import Image
from src import fs
from src.http.url_normalizer import normalize_uri
from src.crypt.puzzle import Puzzle
from src.crypt import sunday_webry_com
from src.base_classes import WebDriver


files_paths = [
    ['/img1.jpg', '/temp/img1.jpg'],
    ['/img2.png', '/temp/img2.png'],
    ['/img3.jpg', '/temp/img3.jpg'],
    ['/img4.jpg', '/temp/img4.jpg'],
    ['/img5.png', '/temp/img5.png'],
    ['/img6.gif', '/temp/img6.gif'],
    ['/img7.webp', '/temp/img7.webp'],
]


class TestImages(unittest.TestCase):

    def test_manual_crop(self):
        for file in files_paths:
            fs.unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])
            sizes = image.size
            image.close()

            img = Image(root_path + file[0])
            img.crop_manual((10, 0, image.size[0], image.size[1]), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])
            cropped_sizes = cropped_image.size
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    def test_manual_crop_with_offsets(self):
        for file in files_paths:
            fs.unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])
            sizes = image.size
            image.close()

            img = Image(root_path + file[0])
            img.crop_manual_with_offsets((10, 0, 0, 0), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])
            cropped_sizes = cropped_image.size
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    def test_auto_crop1(self):
        file = files_paths[0]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] > cropped_sizes[0])

    def test_auto_crop2(self):
        file = files_paths[1]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] == cropped_sizes[0])

    def test_auto_crop3(self):
        file = files_paths[4]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] == (2 + cropped_sizes[0]))  # 2px black line

    def test_image_not_found(self):
        self.assertRaises(AttributeError, lambda: Image(root_path))

    def test_gray1(self):
        file = files_paths[1]
        fs.unlink(root_path + file[1])

        image = Image(root_path + file[0])
        image.gray(root_path + file[1])
        image.close()

        image = PilImage.open(root_path + file[1])
        index = image.mode.find('L')
        image.close()

        self.assertTrue(index == 0)

    def test_convert(self):
        file = files_paths[0][0]
        image = Image(root_path + file)

        basename = file[0:file.find('.')]
        basename = root_path + '/temp' + basename + '.bmp'
        image.convert(basename)
        image.close()

        self.assertTrue(path.isfile(basename))


class TestInitProvider(unittest.TestCase):

    # success
    def test_get_provider1(self):
        provider = get_provider('http://readmanga.me/manga/name/here')
        self.assertIsInstance(provider(), Provider)

    # failed
    def test_get_provider2(self):
        provider = get_provider('http://example.org/manga/name/here')
        self.assertFalse(provider)

    def test_root_path(self):
        self.assertEqual(path.realpath(fs.path_join(root_path, '..')), fs.get_current_path())

    def test_file_name_query_remove(self):
        name = '/addr/to/filename'
        self.assertEqual(
            name,
            fs.remove_file_query_params(name + '?query=params').replace('\\', '/')  # windows os patch
        )


class TestBaseClass(unittest.TestCase):

    def test_base0(self):
        bp = Base()
        domain = 'http://example.org'
        bp._params['url'] = domain + '/manga/here.html'
        self.assertEqual(bp._params['url'], bp.get_url())
        self.assertEqual(domain, bp.domain)

    def test_base1(self):
        bp = Base()
        self.assertRaises(KeyError, bp.get_url)

    def test_autocrop(self):
        bp = Base()
        img = files_paths[0]
        fs.unlink(root_path + img[1])
        bp.image_auto_crop(root_path + img[0], root_path + img[1])
        self.assertTrue(fs.is_file(root_path + img[1]))

    def test_manualcrop0(self):
        bp = Base()
        img = files_paths[0]
        fs.unlink(root_path + img[1])
        bp._image_params['crop'] = (10, 2, 100, 100)
        bp.image_manual_crop(root_path + img[0], root_path + img[1])
        self.assertTrue(fs.is_file(root_path + img[1]))

    def test_manualcrop1(self):
        bp = Base()
        img = files_paths[0]
        fs.unlink(root_path + img[1])
        bp._image_params['offsets_crop'] = (10, 32, 12, 5)
        bp.image_manual_crop(root_path + img[0], root_path + img[1])
        self.assertTrue(fs.is_file(root_path + img[1]))

    def test_get(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/get'
        self.assertEqual(url, json.loads(bp.http_get(url))['url'])

    def test_post(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/post'
        self.assertEqual(url, json.loads(bp.http_post(url))['url'])

    def test_cookies0(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/cookies'
        cookies = {'test': 'test-cookie'}
        self.assertEqual(cookies, json.loads(bp.http_get(url, cookies=cookies))['cookies'])

    def test_cookies1(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/cookies/set?test=test-cookie'
        self.assertEqual('test-cookie', bp.http().get_base_cookies(url).get('test'))

    def test_redirect0(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/redirect-to?url=https://httpbin.org/get?test=1'
        test_data = {'test': '1'}
        self.assertEqual(test_data, json.loads(bp.http_get(url))['args'])

    def test_redirect1(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = 'https://httpbin.org/redirect/11'
        self.assertRaises(AttributeError, bp.http_get, url)

    def test_ascii(self):
        string = '⼢⼣⼤abcde123@#$йцуڪڦ'
        normal_string = 'abcde123@'
        self.assertEqual(Static.remove_not_ascii(string), normal_string)


class TestArchive(unittest.TestCase):

    def test_make_archive(self):
        arc = Archive()
        arc_path = root_path + '/temp/arc.zip'
        fs.unlink(arc_path)
        orig_size = 0
        for idx, item in enumerate(files_paths):
            fs.unlink(root_path + item[1])
            copyfile(root_path + item[0], root_path + item[1])
            orig_size += int(fs.file_size(root_path + item[1]))
            arc.add_file(root_path + item[1])
        arc.add_file(root_path + 'archive_test_file')
        arc.add_file(root_path + 'archive_test_image')
        arc.make(arc_path)
        size = fs.file_size(arc_path)
        self.assertTrue(size and 1024 < int(size) < orig_size)


class TestHttpClasses(unittest.TestCase):
    referer = 'http://example.org/manga/here.html'

    def test_url_normalizer_url_helper1(self):
        url = '//example.org/manga/here.html'
        test_url = normalize_uri(url, self.referer)
        self.assertEqual(self.referer, test_url)

    def test_url_normalizer_url_helper2(self):
        url = '/manga/here.html'
        test_url = normalize_uri(url, self.referer)
        self.assertEqual(self.referer, test_url)

    def test_url_normalizer_url_helper3(self):
        url = '://example.org/manga/here.html'
        test_url = normalize_uri(url, self.referer)
        self.assertEqual(self.referer, test_url)

    def test_url_normalizer_url_helper4(self):
        url = 'here.html'
        test_url = normalize_uri(url, self.referer)
        self.assertEqual(self.referer, test_url)


class TestGhPages(unittest.TestCase):
    def test_make(self):
        from helpers.gh_pages import main
        main()


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


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = WebDriver().get_driver()
        driver.get('http://httpbin.org')
        elements = driver.find_elements_by_css_selector('#manpage ul > li > a')
        count = len(elements)
        driver.close()
        display.stop()
        self.assertTrue(count > 0)


if __name__ == '__main__':
    fs.make_dirs(root_path + '/temp')
    unittest.main()
