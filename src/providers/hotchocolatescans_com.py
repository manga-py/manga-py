from src.providers.gomanga_co import GoMangaCo


class HotChocolateScansCom(GoMangaCo):
    _name_re = '/fs/[^/]+/([^/]+)/'
    _content_str = '{}/fs/series/{}/'

    def _get_json_selector(self, content):
        return r'var\spages\s*=\s*(\[.+\])'


main = HotChocolateScansCom
