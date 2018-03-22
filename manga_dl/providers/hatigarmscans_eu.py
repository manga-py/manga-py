from .read_powermanga_org import ReadPowerMangaOrg


class HatigarmScansEu(ReadPowerMangaOrg):
    _name_re = '/hs/[^/]+/([^/]+)'
    _content_str = '{}/hs/series/{}/'
    _chapters_selector = '.list-group-item .title a'


main = HatigarmScansEu
