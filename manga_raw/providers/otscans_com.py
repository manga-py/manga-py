from .gomanga_co import GoMangaCo


class OtScansCom(GoMangaCo):
    _name_re = '/foolslide/[^/]+/([^/]+)/'
    _content_str = '{}/foolslide/series/{}/'
    _chapters_selector = '.list .group .element .title a'


main = OtScansCom
