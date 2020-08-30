from manga_py.providers.rawdevart_com_old import RawDevArtComOld
from .helpers.std import Std


class MangaTrueCom(RawDevArtComOld, Std):
    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/[^\d]*((?:\d+-?)+\d*)')
        idx = re.search(self.chapter).group(1).split('-')
        return '-'.join(idx[:int(len(idx) / 2 + .5)])

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image img.img-responsive', 'data-src')


main = MangaTrueCom
