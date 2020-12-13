from manga_py.provider import Provider
from .helpers.std import Std


class SoMangaNet(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile('/leitor/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/[^/]+/([^/]+)')

    def get_chapters(self):
        return self._elements('ul.capitulos li > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.img-manga')

    def get_cover(self):
        return self._cover_from_content('.manga .col-sm-4 .img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = SoMangaNet
