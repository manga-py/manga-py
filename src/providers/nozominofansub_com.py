from src.providers.komikid_com import KomikIdCom
from .helpers.std import Std


class NozomiNoFansubCom(KomikIdCom, Std):
    _content_str = '{}/public/manga/{}'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/.+?(\d+(?:[^\d/]\d+)?)')
        ch = self.chapter
        return re.search(ch).group(1)


main = NozomiNoFansubCom
