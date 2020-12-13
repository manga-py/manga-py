from manga_py.provider import Provider
from .helpers.std import Std


class MangaHeavenClub(Provider, Std):
    def get_chapter_index(self) -> str:
        ch = self.re.search(r'-chapter-(\d+(?:\.\d+)?)', self.chapter)
        return ch.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/read-manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/read-manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter > a')

    def get_files(self):
        parser = self.html_fromstring('%s/0' % self.chapter)
        return self._images_helper(parser, '.page-chapter > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.detail-info img')


main = MangaHeavenClub
