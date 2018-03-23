#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import unittest
from os import path

from manga_raw.base_classes import Base, Static
from manga_raw import fs

root_path = path.dirname(path.realpath(__file__))

files_paths = [
    ['/img1.jpg', '/temp/img1.jpg'],
    ['/img2.png', '/temp/img2.png'],
    ['/img3.jpg', '/temp/img3.jpg'],
    ['/img4.jpg', '/temp/img4.jpg'],
    ['/img5.png', '/temp/img5.png'],
    ['/img6.gif', '/temp/img6.gif'],
    ['/img7.webp', '/temp/img7.webp'],
]


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
