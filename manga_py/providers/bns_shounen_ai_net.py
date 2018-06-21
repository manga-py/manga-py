from .read_powermanga_org import ReadPowerMangaOrg


class BnsShounenAiNet(ReadPowerMangaOrg):
    _name_re = '/read/[^/]+/([^/]+)/'
    _content_str = '{}/read/series/{}/'


main = BnsShounenAiNet
