from .read_powermanga_org import ReadPowerMangaOrg


class AdultoSeinagiOrg(ReadPowerMangaOrg):
    _name_re = '[^/]/[^/]+/([^/]+)/'
    _content_str = '{}/series/{}/'


main = AdultoSeinagiOrg
