from .zmanga_net import ZMangaNet


class MangaHiNet(ZMangaNet):
    _type = 'chapter'


main = MangaHiNet
