from manga_py.provider import Provider
from .helpers.std import Std


class ReMangaOrg(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/vol(\d+)/(\d+(?:\.\d+)?)', self.chapter)
        return '{}-{}'.format(
            *idx.groups()
        ).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter-list a.row')

    def get_files(self):
        n = self.http().normalize_uri
        content = self.http_get(self.chapter)
        match = self.re.search('all_pages = (\[.+?\]);', content).group(1)
        images = self.json.loads(match.replace("'", '"'))
        return [n(i.get('link')) for i in images]

    def get_cover(self) -> str:
        return self._cover_from_content('.item img.head')


main = ReMangaOrg
