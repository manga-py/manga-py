from .mangago_me import MangaGoMe


class RocacaCom(MangaGoMe):

    def get_chapter_index(self) -> str:
        re = self.re.search(r'/.+?chapter-(\d+(?:\.\d+)?)', self.chapter)
        if not re:
            re = self.re.search(r'/.+?Ch(\d+(?:\.\d+)?)', self.chapter)
        if not re:
            re = self.re.search(r'/c(\d+(?:\.\d+)?)', self.chapter)
        if not re:
            re = self.re.search(r'/(\d+(?:\.\d+)?)/', self.chapter)
        return re.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.section-list > table a.chico')

    def get_cover(self) -> str:
        return self._cover_from_content('.cartoon-intro > img.pic')


main = RocacaCom
