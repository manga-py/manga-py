# from manga_py.fs import dirname, path_join, get_temp_path, rename
from manga_py.provider import Provider
from .helpers.std import Std, Http2


class MangaChanMe(Provider, Std):
    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        name = r'\.me/[^/]+/\d+-(.+)\.html'
        return self._get_name(name)

    def loop_chapters(self):
        items = self._storage['chapters'][::-1]
        n = self.http().normalize_uri
        Http2(self).download_archives([n(i) for i in items])

    def get_chapters(self):
        selector = r'\.me/[^/]+/(\d+-.+\.html)'
        url = self._get_name(selector)
        url = '{}/download/{}'.format(self.domain, url)
        return self.html_fromstring(url, 'table#download_table tr td + td > a')

    def get_files(self):
        return []

    def get_cover(self):
        selector = r'\.me/[^/]+/(\d+-.+\.html)'
        url = self._get_name(selector)
        url = '{}/manga/{}'.format(self.domain, url)
        img = self._elements('#cover', self.http_get(url))
        if img and len(img):
            return img[0].get('src')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaChanMe
