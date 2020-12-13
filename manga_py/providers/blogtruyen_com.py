from manga_py.provider import Provider
from .helpers.std import Std


class BlogTruyenCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.\w{2,7}/c(\d+)/', self.chapter)
        return '{}-{}'.format(self.chapter_id, idx.group(1))

    def get_content(self):
        url = self._test_main_url(self.get_url())
        return self.http_get(self.http().normalize_uri(url))

    def _test_main_url(self, url):
        if self._test_url(url, r'/c'):
            selector = '.breadcrumbs a + a'
            url = self.html_fromstring(url, selector, 0).get('href')
        return url

    def get_manga_name(self) -> str:
        url = self._test_main_url(self.get_url())
        return self.re.search(r'/\d+/([^/]+)', url).group(1)

    def get_chapters(self):
        return self._elements('#list-chapters .title > a')

    def get_files(self):
        items = self.html_fromstring(self.chapter, '#content img')
        return [i.get('src') for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.thumbnail img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = BlogTruyenCom
