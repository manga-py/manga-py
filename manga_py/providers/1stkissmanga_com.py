from .rawdevart_com import RawDevArtCom


class FirstKissMangaCom(RawDevArtCom):
    _chapter_selector = r'/manga/[^/]+/chapter-(\d+(?:-\d+)?)'

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img[data-src]', attr='data-src')


main = FirstKissMangaCom
