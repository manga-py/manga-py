from src.providers.mangashiro_net import MangaShiroNet


class SubaPicsCom(MangaShiroNet):
    alter_re_name = r'\.com/([^/]+)\-chapter-\d+'
    chapter_re = r'\-chapter\-(\d+(?:\-\d+)?)'

    def get_cover(self) -> str:
        return self._get_cover_from_content('.imgdesc > img')

    def get_files(self):
        url = self.get_current_chapter()
        parser = self.html_fromstring(url)
        items = parser.cssselect('#readerarea img')
        return [i.get('src') for i in items]


main = SubaPicsCom
