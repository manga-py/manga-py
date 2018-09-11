from manga_py.provider import Provider
from .helpers.std import Std


class ManhwaCo(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        return self.re.search(r'\.co/[^/]+/([^/]+)', chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.co/([^/]+)')

    def get_chapters(self):
        return self._elements('.list-group .list-group-item')

    def get_files(self):
        content = self.http_get(self.chapter)
        return self._images_helper(content, 'img.img-fluid')

    def get_cover(self) -> str:
        return self._cover_from_content('.row > div > img.img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ManhwaCo
