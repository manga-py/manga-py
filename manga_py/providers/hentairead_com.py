from .helpers.std import Std
from .readhentaimanga_com import ReadHentaiMangaCom


class HentaiReadCom(ReadHentaiMangaCom, Std):

    def get_chapters(self):
        return self._elements('.read-now a.lst')


main = HentaiReadCom
