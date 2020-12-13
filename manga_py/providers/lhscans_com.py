from manga_py.provider import Provider
from .helpers.std import Std


class LhScansCom(Provider, Std):
    def get_chapter_index(self) -> str:
        re = self.re.compile(r'-chapter-(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga-{}.html')

    def get_manga_name(self) -> str:
        return self._get_name(r'(?:read|manga)-(.+?)(?:-chapter-.+)?.html')

    def get_chapters(self):
        return self._elements('a.chapter')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.chapter-content .chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.thumbnail img')

    def book_meta(self) -> dict:
        pass


main = LhScansCom
