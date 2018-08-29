from .read_powermanga_org import ReadPowerMangaOrg


class TripleSevenScansCom(ReadPowerMangaOrg):
    _name_re = '/reader/[^/]+/([^/]+)/'
    _content_str = '{}/reader/series/{}/'


main = TripleSevenScansCom
