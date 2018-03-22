from .gomanga_co import GoMangaCo


class HelveticaScansCom(GoMangaCo):
    _name_re = '/r/[^/]+/([^/]+)/'
    _content_str = '{}/r/series/{}/'


main = HelveticaScansCom
