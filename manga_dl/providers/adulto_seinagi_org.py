from .pzykosis666hfansub_com import Pzykosis666HFansubCom


class AdultoSeinagiOrg(Pzykosis666HFansubCom):
    _name_re = '[^/]/[^/]+/([^/]+)/'
    _content_str = '{}/series/{}/'


main = AdultoSeinagiOrg
