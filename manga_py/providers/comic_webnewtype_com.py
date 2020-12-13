from manga_py.provider import Provider
from .helpers.std import Std


class ComicWebNewTypeCom(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile('/contents/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/contents/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/contents/([^/]+)')

    def get_chapters(self):
        return self._elements('#episodeList li.ListCard a')

    def get_files(self):
        url = self.chapter
        items = self.http_get(url + 'json/', headers={'x-requested-with': 'XMLHttpRequest'})
        imgs = self.json.loads(items)
        imgs = [self.re.sub(r'jpg.+', 'jpg', img) for img in imgs]
        return imgs

    def get_cover(self) -> str:
        return self._cover_from_content('.WorkSummary-content img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ComicWebNewTypeCom
