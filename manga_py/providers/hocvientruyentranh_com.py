from manga_py.provider import Provider
from .helpers.std import Std


class HocVienTruyenTranhCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/chapter/(\d+)', self.chapter)
        return '{}-{}'.format(self.chapter_id, idx.group(1))

    def _test_main_url(self, url):
        if self.re.search('/chapter/', url):
            url = self.html_fromstring(url, '#subNavi a', 0).get('href')
        return url

    def get_main_content(self):
        url = self._test_main_url(self.get_url())
        return self.http_get(self.http().normalize_uri(url))

    def get_manga_name(self) -> str:
        url = self._test_main_url(self.get_url())
        return self.re.search('/manga/[^/]+/([^/]+)', url).group(1)

    def get_chapters(self):
        return self._elements('.table-scroll table.table td > a')

    def get_files(self):
        selector = '.manga-container img.page'
        items = self.html_fromstring(self.chapter, selector)
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('.__info-container .__image img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = HocVienTruyenTranhCom
