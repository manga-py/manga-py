from .helpers.std import Std
from .rawdevart_com import RawDevArtCom


class RawNekoCom(RawDevArtCom, Std):
    _chapter_selector = r'/chapter-(\d+(?:-\d+)?)'


main = RawNekoCom
