from .komikid_com import KomikIdCom


class NozomiNoFansubCom(KomikIdCom):
    _content_str = '{}/public/manga/{}'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/.+?(\d+(?:[^\d/]\d+)?)')
        split = self.re.compile(r'[^\d+]')
        return '-'.join(split.split(re.search(self.chapter).group(1)))


main = NozomiNoFansubCom
