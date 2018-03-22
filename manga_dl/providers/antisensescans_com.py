from .read_powermanga_org import ReadPowerMangaOrg


class AntiSenseScansCom(ReadPowerMangaOrg):
    _name_re = '/online/[^/]+/([^/]+)/'
    _content_str = '{}/online/series/{}/'


main = AntiSenseScansCom
