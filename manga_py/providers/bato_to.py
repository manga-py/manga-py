from manga_py.provider import Provider
from .helpers.std import Std


class BatoTo(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}-{}'.format(
            self.chapter_id,
            self.chapter[1]
        )

    def get_chapter_index(self) -> str:
        return self.re.search(r'/chapter/(\d+)', self.chapter[0]).group(1)

    def get_main_content(self):
        url = self.get_url()
        if ~url.find('/chapter/'):
            url = self.html_fromstring(url, '.nav-path .nav-title > a', 0).get('href')
        return self.http_get(url)

    def get_manga_name(self) -> str:
        selector = '.nav-path .nav-title > a,.title-set .item-title > a'
        return self.html_fromstring(self.get_url(), selector, 0).text_content()

    def get_chapters(self):
        items = self._elements('.main > .item > a')
        n = self.http().normalize_uri
        return [(n(i.get('href')), i.cssselect('b')[0].text_content().strip(' \n\t\r')) for i in items]

    @staticmethod
    def _sort_files(data):
        keys = sorted(data, key=lambda _: _)
        return [data[i] for i in keys]

    def get_files(self):
        data = self.re.search(r'\simages\s*=\s*({.+});', self.http_get(self.chapter[0]))
        try:
            return self._sort_files(self.json.loads(data.group(1)))
        except ValueError:
            return []

    def get_cover(self) -> str:
        return self._cover_from_content('.attr-cover img')


main = BatoTo
