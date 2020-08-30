from .helpers.std import Std
from .rawdevart_com_old import RawDevArtComOld


class RawNekoCom(RawDevArtComOld, Std):
    _chapter_selector = r'/chapter-(\d+(?:-\d+)?)'


main = RawNekoCom
