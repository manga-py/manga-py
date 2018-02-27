from src.provider import Provider
from .helpers.std import Std


class RawDevArtCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}'
        return fmt.format(*idx)

    def get_chapter_index(self) -> str:
        ch = self.get_current_chapter()
        idx = self.re.search(r'/chapter/[^\d]+(\d+(?:\.\d+)?)', ch)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.wp-manga-chapter > a')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        return self._images_helper(parser, '.page-break img.wp-manga-chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image img.img-responsive')


main = RawDevArtCom
