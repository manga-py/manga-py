from manga_py.provider import Provider
from .helpers.std import Std


class RawDevArtCom(Provider, Std):
    _chapter_selector = r'/chapter/[^\d]+(\d+(?:\.\d+)?)'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        ch = self.chapter
        idx = self.re.search(self._chapter_selector, ch)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.wp-manga-chapter > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img.wp-manga-chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image img.img-responsive')


main = RawDevArtCom
