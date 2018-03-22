from .pzykosis666hfansub_com import Pzykosis666HFansubCom


class TripleSevenScansCom(Pzykosis666HFansubCom):
    _name_re = '/reader/[^/]+/([^/]+)/'
    _content_str = '{}/reader/series/{}/'


main = TripleSevenScansCom
