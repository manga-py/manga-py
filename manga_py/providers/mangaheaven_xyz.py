from manga_py.provider import Provider
from .helpers.std import Std


class MangaHeavenXyz(Provider, Std):
    def get_chapter_index(self) -> str:
        ch = self.re.search(r'/chapter-(\d+(?:\.\d+)?)', self.chapter)
        return ch.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.table-scroll > .table td > a')

    def get_files(self):
        parser = self.html_fromstring('%s/0' % self.chapter)
        return self._images_helper(parser, '.manga-container > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.__image > img')


main = MangaHeavenXyz
