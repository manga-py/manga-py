#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path

from manga_py import fs
from manga_py.provider import Provider
from manga_py.providers import get_provider

root_path = path.dirname(path.realpath(__file__))


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
        self.assertEqual(path.realpath(fs.path_join(root_path, '..')), fs.root_path())

    def test_file_name_query_remove(self):
        name = '/addr/to/filename'
        self.assertEqual(
            name,
            fs.remove_file_query_params(name + '?query=params').replace('\\', '/')  # windows os patch
        )
