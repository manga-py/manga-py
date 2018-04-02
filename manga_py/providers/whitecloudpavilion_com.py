from manga_py.provider import Provider
from .helpers.std import Std


class WhiteCloudPavilionCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name(idx.split('.'))

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/free/manga/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/free/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/free/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters .chapter-title-rtl a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        items = self._images_helper(parser, '#all img', 'data-src')
        return [i.strip(' \n\r\t\0') for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed img.img-responsive')


main = WhiteCloudPavilionCom
