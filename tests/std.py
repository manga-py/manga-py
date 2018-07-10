import unittest
from .base import root_path
from manga_py.fs import path_join
from manga_py.providers.helpers.std import Std
from manga_py.provider import Provider


class M(Std, Provider):
    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w+/([^/]+)\?')

    def get_chapters(self) -> list:
        return self._elements('a')

    def get_files(self) -> list:
        parser = self.document_fromstring(self.content)
        return self._images_helper(parser, 'a', 'href')

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'


class StdCase(unittest.TestCase):
    @property
    def _provider(self):
        provider = M()
        provider._params['url'] = 'https://www.google.com/imghp?hl=&tab=wi'
        return provider

    def test_base(self):
        provider = self._provider
        self.assertTrue(provider.get_manga_name() == provider.manga_name)
        self.assertNotIn('manga_name', provider._storage)
        provider._storage['manga_name'] = provider.get_manga_name() + '-name'
        self.assertFalse(provider.get_manga_name() == provider.manga_name)
        self.assertTrue(~provider.manga_name.find('imghp'))
        provider._storage['manga_name'] = provider.get_manga_name()
        self.assertTrue(len(provider.content) > 100)

    def test_cookies(self):
        provider = self._provider
        provider._base_cookies(provider.get_url())
        self.assertTrue(len(provider._storage['cookies'].keys()) > 0)

    def test_normal_name(self):
        name = self._provider.normal_arc_name(['1', '2'])
        self.assertEqual('vol_001-2', name)

    def test_iterators(self):
        provider = self._provider
        provider._storage['manga_name'] = provider.manga_name
        self.assertTrue(len(provider.get_chapters()) > 0)
        self.assertTrue(~provider.get_files()[0].find('.google.'))

    def test_cover_from_content(self):
        self.content = '<html>'
        src = self._provider._cover_from_content('img')
        self.assertEqual('http', src[:4])

    def test_first_select(self):
        provider = self._provider
        with open(path_join(root_path, 'files', 'select.html'), 'r') as f:
            provider._storage['main_content'] = f.read()
        reference = len(provider._elements('select')[0].cssselect('option'))
        parser = provider.document_fromstring(provider.content)
        skip = len(provider._first_select_options(parser, 'select'))
        not_exists = len(provider._first_select_options(parser, 'select#not_exists_selector'))

        self.assertTrue(reference == (skip + 1))
        self.assertTrue(not_exists == 0)
