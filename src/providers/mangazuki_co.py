from src.provider import Provider
from .helpers.std import Std


class MangaZukiCo(Provider, Std):  # NozomiNoFansubCom

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search(r'/manga/[^/]+/(\d+(?:\.\d+)?)', chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        return self._images_helper(parser, '#all > img.img-responsive', 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('img.img-responsive')


main = MangaZukiCo
