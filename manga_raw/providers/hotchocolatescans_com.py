from .gomanga_co import GoMangaCo


class HotChocolateScansCom(GoMangaCo):
    _name_re = '/fs/[^/]+/([^/]+)/'
    _content_str = '{}/fs/series/{}/'


main = HotChocolateScansCom
