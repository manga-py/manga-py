from src.providers.gomanga_co import GoMangaCo


class ReadPowerMangaOrg(GoMangaCo):
    _name_re = '[^/]/[^/]+/([^/]+)'
    _content_str = '{}/series/{}/'

    def get_chapter_index(self) -> str:
        url = self.get_current_chapter()
        index_re = '/rea\\w+/[^/]+/(?:[^/]+/)?(\\d+/\\d+(?:/\\d+)?)'
        group = self.re.search(index_re, url).group(1)
        return group.replace('/', '-')

    def _get_json_selector(self, content):
        return 'var\\spages\\s*=\\s*(\\[.+\\])'


main = ReadPowerMangaOrg
