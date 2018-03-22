from .read_powermanga_org import ReadPowerMangaOrg


class Pzykosis666HFansubCom(ReadPowerMangaOrg):
    _name_re = '/online/[^/]+/([^/]+)/'
    _content_str = '{}/online/series/{}/'


main = Pzykosis666HFansubCom
