from .rawdevart_com import RawDevArtCom
from .helpers.std import Std


class RawNekoCom(RawDevArtCom, Std):
    _chapter_selector = r'/chapter-(\d+(?:-\d+)?)'


main = RawNekoCom
