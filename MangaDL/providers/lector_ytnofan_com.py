from .gomanga_co import GoMangaCo


class LectorYTNoFanCom(GoMangaCo):
    _name_re = '/(?:series|read)/([^/]+)/'
    _content_str = '{}/series/{}/'


main = LectorYTNoFanCom
