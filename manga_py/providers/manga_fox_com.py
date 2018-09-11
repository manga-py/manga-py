from manga_py.provider import Provider
from .helpers.std import Std


class MangaFoxCom(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chapter-(\d+(?:-\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.(?:com|io)/([^/]+)')

    def get_chapters(self):
        return self._elements('.list_chapter a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#list_chapter img')

    def get_cover(self) -> str:
        return self._cover_from_content('.info_image img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaFoxCom
