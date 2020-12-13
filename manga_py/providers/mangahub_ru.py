import html

from manga_py.provider import Provider
from .helpers.std import Std


class MangaHubRu(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/read/[^/]+/[^\d]+(\d+)/(\d+)/', self.chapter).groups()
        return '{}-{}'.format(*idx)

    def get_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)/?')

    def get_chapters(self):
        return self._elements('.d-flex > a[href*="/read/"]')

    def get_files(self):
        parser = self.html_fromstring(self.chapter, 'reader')
        if not parser:
            return []
        result = parser[0].get('data-reader-store')
        result = self.json.loads(html.unescape(result))['scans']
        n = self.http().normalize_uri
        return [n(i['src']) for i in result]

    def get_cover(self):
        return self._cover_from_content('img.cover-detail-img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHubRu
