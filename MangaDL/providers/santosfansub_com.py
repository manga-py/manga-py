from .helveticascans_com import HelveticaScansCom


class SantosFansubCom(HelveticaScansCom):
    _name_re = '/slide/[^/]+/([^/]+)/'
    _content_str = '{}/slide/series/{}/'


main = SantosFansubCom
