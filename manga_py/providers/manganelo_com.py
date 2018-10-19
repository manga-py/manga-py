from manga_py.provider import Provider
from .helpers.std import Std


class MangaNeloCom(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chap(?:ter)?_(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter-list a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        images = self._images_helper(parser, '#vungdoc img')
        if not len(images):
            images = self._images_helper(parser, '.vung_doc img')
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-info-pic img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaNeloCom
