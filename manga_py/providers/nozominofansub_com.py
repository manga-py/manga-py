from .komikid_com import KomikIdCom


class NozomiNoFansubCom(KomikIdCom):
    _content_str = '{}/public/manga/{}'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/.+?(\d+(?:[^\d/]\d+)?)')
        ch = self.chapter
        return re.search(ch).group(1)


main = NozomiNoFansubCom
