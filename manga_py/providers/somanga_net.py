from manga_py.provider import Provider
from .helpers.std import Std


class SoMangaNet(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return self.re.search('/leitor/[^/]+/([^/]+)').group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.net/[^/]+/([^/]+)')

    def get_chapters(self):
        return self.document_fromstring(self.content, 'ul.capitulos li > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter, 'img.img-manga')
        return [i.get('src') for i in parser]

    def get_cover(self):
        pass  # FIXME HOME


main = SoMangaNet
