# from manga_py.fs import dirname, path_join, get_temp_path, rename
from manga_py.provider import Provider
from .helpers.std import Std
from .helpers._http2 import Http2


class MangaChanMe(Provider, Std):
    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_content(self):
        pass

    def get_manga_name(self) -> str:
        name = r'\.\w{2,7}/[^/]+/\d+-(.+)\.html'
        return self._get_name(name)

    def loop_chapters(self):
        # Could not test, website does not seem to exist anymore...
        # previously there was a normalize_uri on every chapters,
        # but it should already be handled in __normalize_chapters in Base class
        Http2(self).download_archives()

    def get_chapters(self):
        selector = r'\.\w{2,7}/[^/]+/(\d+-.+\.html)'
        url = self._get_name(selector)
        url = '{}/download/{}'.format(self.domain, url)
        return self.html_fromstring(url, 'table#download_table tr td + td > a')[::-1]

    def get_files(self):
        return []

    def get_cover(self):
        selector = r'\.\w{2,7}/[^/]+/(\d+-.+\.html)'
        url = '{}/manga/{}'.format(self.domain, self._get_name(selector))
        img = self._elements('#cover', self.http_get(url))
        if img and len(img):
            return img[0].get('src')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaChanMe
