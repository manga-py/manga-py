from .gomanga_co import GoMangaCo
from .helpers.std import Std


class RiceBallIciousInfo(GoMangaCo, Std):
    _name_re = '/fs/reader/[^/]+/([^/]+)/'
    _content_str = '{}/fs/reader/series/{}/'


main = RiceBallIciousInfo
