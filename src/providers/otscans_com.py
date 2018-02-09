from src.providers.gomanga_co import GoMangaCo


class OtScansCom(GoMangaCo):
    _name_re = '/foolslide/[^/]+/([^/]+)/'
    _content_str = '{}/foolslide/series/{}/'
    _chapters_selector = '.list .group .element .title a'

    def _get_json_selector(self, content):
        return r'var\spages\s*=\s*(\[.+\])'


main = OtScansCom
