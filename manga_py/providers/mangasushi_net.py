from .rawdevart_com_old import RawDevArtComOld


class MangaSushiNet(RawDevArtComOld):
    _chapter_selector = r'/chapter-(\d+(?:-\d+)?)'

    def get_chapter_index(self) -> str:
        idx = self.re.search(self._chapter_selector, self.chapter)
        return idx.group(1)

    def get_files(self):
        chapter = self.chapter.replace('p/1/', '').replace('?style=paged', '') + '?style=list'
        parser = self.html_fromstring(chapter)
        _class = '.page-break img.wp-manga-chapter-img'
        return self._images_helper(parser, _class, 'data-src')


main = MangaSushiNet
