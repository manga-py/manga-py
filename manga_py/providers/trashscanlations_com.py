from .zeroscans_com import ZeroScansCom


class TrashScanlationsCom(ZeroScansCom):
    def get_chapter_index(self) -> str:
        ch = self.chapter
        idx = self.re.search(self._chapter_selector, ch)
        idx = self.re.split(r'[^\d]', idx.group(1))
        return '-'.join(idx)

    def get_main_content(self):
        return self._get_content('{}/series/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/series/([^/]+)')


main = TrashScanlationsCom
