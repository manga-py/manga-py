from .pzykosis666hfansub_com import Pzykosis666HFansubCom


class BnsShounenAiNet(Pzykosis666HFansubCom):
    _name_re = '/read/[^/]+/([^/]+)/'
    _content_str = '{}/read/series/{}/'


main = BnsShounenAiNet
