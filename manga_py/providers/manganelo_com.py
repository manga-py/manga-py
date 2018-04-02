from manga_py.provider import Provider
from .helpers.std import Std


class MangaNeloCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name(idx.split('.', 2))

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chapter_(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter-list a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#vungdoc img')

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-info-pic img')


main = MangaNeloCom
