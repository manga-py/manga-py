from src.providers.gomanga_co import GoMangaCo


class ReadPowerMangaOrg(GoMangaCo):
    _name_re = '[^/]/[^/]+/([^/]+)'
    _content_str = '{}/series/{}/'

    def _get_json_selector(self, content):
        return 'var\\spages\\s*=\\s*(\\[.+\\])'


main = ReadPowerMangaOrg
