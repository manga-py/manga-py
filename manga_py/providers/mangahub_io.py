from manga_py.provider import Provider
from .helpers.std import Std


class MangaHubIo(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        return self.re.search(r'/chapter/[^/]+/\w+-([^/]+)', chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.list-group .list-group-item > a')

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self._elements('#mangareader img[src*="/file/"]', content)
        n = self.http().normalize_uri
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.row > div > img.img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHubIo
