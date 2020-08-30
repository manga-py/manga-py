from .rawdevart_com_old import RawDevArtComOld


class ManhwaReaderCom(RawDevArtComOld):
    _chapter_selector = r'/chapter-(\d+(?:[^\d]\d+)?)'

    def get_chapter_index(self) -> str:
        ch = self.chapter
        idx = self.re.search(self._chapter_selector, ch)
        idx = idx.group(1)
        test = self.re.search(r'(\d+)[^\d](\d+)', idx)
        if test:
            return '-'.join(test.groups())
        return idx

    def get_chapters(self):
        items = self._elements('.wp-manga-chapter > a')
        n = self.http().normalize_uri
        return [n(i.get('href')).rstrip('/') + '/?style=list' for i in items]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img')


main = ManhwaReaderCom
