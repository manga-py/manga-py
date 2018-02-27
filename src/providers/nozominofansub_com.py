from src.provider import Provider
from .helpers.std import Std


class NozomiNoFansubCom(Provider, Std):  # MangaZukiCo

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('.', 2)
        re = 'vol_{:0>3}'
        if len(idx) > 1:
            re += '-{}'
        return re.format(*idx)

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/.+?(\d+(?:[^\d/]\d+)?)')
        ch = self.get_current_chapter()
        return re.search(ch).group(1)

    def get_main_content(self):
        return self._get_content('{}/public/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/public(?:/index.php)?/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter-title-rtl > a')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        return self._images_helper(parser, '#all img.img-responsive', 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed .img-responsive')


main = NozomiNoFansubCom
