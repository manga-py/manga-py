from .gomanga_co import GoMangaCo


class LectorKirishimaFanSubCom(GoMangaCo):
    _name_re = '/(?:reader/)?(?:series|read)/([^/]+)/'
    _content_str = '{}/lector/series/{}/'


main = LectorKirishimaFanSubCom
