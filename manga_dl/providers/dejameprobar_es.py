from manga_dl.providers.helveticascans_com import HelveticaScansCom


class DejameProbarEs(HelveticaScansCom):
    _name_re = '/slide/[^/]+/([^/]+)/'
    _content_str = '{}/slide/series/{}/'


main = DejameProbarEs
