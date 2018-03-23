from manga_py.provider import Provider
from .helpers.std import Std


class MangaEdenCom(Provider, Std):
    uriRegex = r'/[^/]+/([^/]+-manga)/([^/]+)/?'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'-manga/[^/]+/(\d+)', self.chapter).group(1)
        return '{}-0'.format(idx)

    def get_main_content(self):
        result = self.re.search(self.uriRegex, self.get_url())
        groups = result.groups()
        return self.http_get('{}/en/{}/{}/'.format(self.domain, *groups))

    def get_manga_name(self) -> str:
        return self.re.search(self.uriRegex, self.get_url()).group(2)

    def get_chapters(self):
        return self._elements('a.chapterLink')

    def get_files(self):
        content = self.http_get(self.chapter)
        result = self.re.search(r'var\s+pages\s+=\s+(\[{.+}\])', content)
        items = []
        if not result:
            return []
        for i in self.json.loads(result.group(1)):
            items.append('http:' + i['fs'])
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('#rightContent .info img')


main = MangaEdenCom
