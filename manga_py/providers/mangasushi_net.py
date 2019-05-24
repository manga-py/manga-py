from .rawdevart_com import RawDevArtCom


class MangaSushiNet(RawDevArtCom):
    _chapter_selector = r'/chapter-(\d+(?:-\d+)?)'

    def get_chapter_index(self) -> str:
        idx = self.re.search(self._chapter_selector, self.chapter)
        return idx.group(1)

    @property
    def chapter(self):
        return super().chapter.replace('?style=paged', '?style=list')


main = MangaSushiNet
