from manga_py.provider import Provider
from .helpers.std import Std


class MangaKakalotCom(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.search('/chapter_([^/]+)', self.chapter)
        return re.group(1).replace('.', '-', 2)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)/?')

    def get_chapters(self):
        return self._elements('.chapter-list span a')

    def get_files(self):
        result = self.html_fromstring(self.chapter, '#vungdoc img')
        return [i.get('src') for i in result]

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaKakalotCom
