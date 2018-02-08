from src.providers.gomanga_co import GoMangaCo


class HelveticaScansCom(GoMangaCo):
    _name_re = '/r/[^/]+/([^/]+)/'
    _content_str = '{}/r/series/{}/'

    def _get_json_selector(self, content):
        return 'var\\spages\\s*=\\s*(\\[.+\\])'


main = HelveticaScansCom
