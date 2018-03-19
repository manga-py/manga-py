from src.providers.rawdevart_com import RawDevArtCom


class ZeroScansCom(RawDevArtCom):
    _chapter_selector = r'/chapter-(\d+(?:\.\d+)?)'

    def get_chapters(self):
        items = self._elements('.wp-manga-chapter > a')
        n = self.http().normalize_uri
        return [n(i) + '?style = list' for i in items]

    def get_files(self):
        parser = self.http_get(self.chapter)
        return self._images_helper(parser, '.page-break > img')


main = ZeroScansCom
