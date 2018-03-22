from .gomanga_co import GoMangaCo


class ReadPowerMangaOrg(GoMangaCo):
    _name_re = '[^/]/[^/]+/([^/]+)'
    _content_str = '{}/series/{}/'

    def get_chapter_index(self) -> str:
        url = self.chapter
        index_re = r'/rea\w+/[^/]+/(?:[^/]+/)?(\d+/\d+(?:/\d+)?)'
        group = self.re.search(index_re, url).group(1)
        return group.replace('/', '-')


main = ReadPowerMangaOrg
