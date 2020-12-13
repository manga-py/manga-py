from manga_py.provider import Provider
from .helpers.std import Std
from sys import stderr


class HentaiPornsNet(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        url = self.get_url()
        if ~url.find('/tag/'):
            self.log('Please, use target url', file=stderr)
            exit(1)
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name(r'//[^/]+/([^/]+)')

    def get_chapters(self):
        return [b'']

    def get_files(self):
        parser = self.document_fromstring(self.content)
        return self._images_helper(parser, '.gallery-item a', 'href')

    def get_cover(self) -> str:
        return self._cover_from_content('.post-thumbnail img')


main = HentaiPornsNet
