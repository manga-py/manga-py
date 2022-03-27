from manga_py.provider import Provider
from .helpers.std import Std


class JManaNet(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.books-db-detail a.tit')

    def get_chapters(self):
        idx = len(self.manga_name)
        return [self.__chapter(i, idx) for i in self._elements('.books-list-detail .lst-wrap li a')]

    def get_files(self):
        parser = self.document_fromstring(self.http_get(self.chapter[0]))
        return self._images_helper(parser, 'img.comicdetail', 'data-src', 'src')

    def __chapter(self, element, idx: int):
        return (
            self.http().normalize_uri(element.get('href')),
            self.element_text_content(element)[idx:].strip(),
        )

    def get_cover(self) -> str:
        return self._cover_from_content('.books-thumnail img')

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = JManaNet
