import unittest
from os import path

from manga_py import fs
from manga_py.provider import Provider
from manga_py.providers import get_provider

root_path = path.dirname(path.realpath(__file__))


class TestInitProvider(unittest.TestCase):

    # success
    def test_get_provider1(self):
        provider = get_provider('http://readmanga.live/manga/name/here')
        self.assertIsInstance(provider(), Provider)

    # failed
    def test_get_provider2(self):
        provider = get_provider('http://example.org/manga/name/here')
        self.assertFalse(provider)

    def test_root_path(self):
        self.assertEqual(path.realpath(fs.path_join(root_path, '..')), fs.root_path())

    def test_file_name_query_remove1(self):
        name = '/addr/to/filename'
        self.assertEqual(
            name,
            fs.remove_file_query_params(name + '?query=params').replace('\\', '/')  # windows os patch
        )

    def test_file_name_query_remove2(self):
        name = '/addr/to/filename/'
        self.assertEqual(
            name + 'image.png',
            fs.remove_file_query_params(name + '?query=params').replace('\\', '/')  # windows os patch
        )
