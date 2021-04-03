from .rawdevart_com_old import RawDevArtComOld


class ISekaiScanCom(RawDevArtComOld):
    _chapter_selector = r'/manga/[^/]+/(?:chapter-)?(\d+(?:[\a-zA-Z\.-]*?\d+)?(?:-\w+)?)/'

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img.wp-manga-chapter-img', 'data-src', 'src')


main = ISekaiScanCom
