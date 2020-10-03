from .rawdevart_com_old import RawDevArtComOld


class ISekaiScanCom(RawDevArtComOld):
    _chapter_selector = r'/(?:chapter-)?(\d+(?:[\a-zA-Z\.-]*?\d+)?(?:-\w+)?)/'

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img.wp-manga-chapter-img', 'data-src')


main = ISekaiScanCom
