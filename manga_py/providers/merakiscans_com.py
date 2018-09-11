from manga_py.provider import Provider
from .helpers.std import Std


class MerakiScansCom(Provider, Std):
    _name_re = 'com/([^/]+)'
    _content_str = '{}/{}/'

    def get_chapter_index(self) -> str:
        re = self.re.compile(self._name_re + '/([^/]+)')
        idx = re.search(self.chapter).group(2)
        return '-'.join(idx.split('.'))

    def _home_url(self):
        return self._content_str.format(self.domain, self.manga_name)

    def get_main_content(self):
        return self.http_get(self._home_url())

    def get_manga_name(self) -> str:
        return self._get_name(self._name_re)

    def _get_pages_count(self):
        items = self._elements('.pgg li:last-child > a')
        if items and len(items):
            href = items[0].get('href')
            re = self.re.compile(r'/chapter-list/(\d[^/]*)')
            return int(re.search(href).group(1))
        return 1

    def get_chapters(self):
        selector = 'ul.lst li > a'
        pages = self._get_pages_count()
        items = self._elements(selector)
        for i in range(1, pages):
            url = '{}/chapter-list/{}/'.format(self._home_url(), i + 1)
            content = self.http_get(url)
            items += self._elements(selector, content)
        return items

    def get_files(self):
        content = self.http_get(self.chapter)
        return self._images_helper(content, '#longWrap img')

    def get_cover(self) -> str:
        return self._cover_from_content('.mng_ifo img.cvr')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MerakiScansCom
