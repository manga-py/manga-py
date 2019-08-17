import html

from manga_py.provider import Provider
from .helpers.std import Std


class MangaHubRu(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/read/[^/]+/[^\d]+(\d+)/(\d+)/', self.chapter).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.ru/([^/]+)/?')

    def get_chapters(self):
        return self._elements('.b-catalog-list__name a[href^="/"]')

    def get_files(self):
        parser = self.html_fromstring(self.chapter, '.b-main-container .b-reader__full')
        if not parser:
            return []
        result = parser[0].get('data-js-scans')
        result = self.json.loads(html.unescape(result.replace(r'\/', '/')))
        n = self.http().normalize_uri
        return [n(i['src']) for i in result]

    def get_cover(self):
        return self._cover_from_content('.manga-section-image__img img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHubRu
