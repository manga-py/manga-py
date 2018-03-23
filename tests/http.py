#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from manga_py.http.url_normalizer import normalize_uri


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
