from manga_py.provider import Provider
from .helpers.std import Std


class MangaEdenCom(Provider, Std):
    uriRegex = r'/([^/]+)/[^/]+-manga/([^/]+)/?'
    apiUri = '{}/api/{}/{}/'  # (domain, chapter|manga,
    __lang = 'en'
    __cdn_url = 'https://cdn.mangaeden.com/mangasimg/'

    def get_chapter_index(self) -> str:
        return str(self.chapter[0]).replace('.', '-')

    def get_main_content(self):
        return self.http_get('{domain}/{lang}/{lang}-manga/{name}/'.format(
            domain=self.domain,
            lang=self.__lang,
            name=self.manga_name,
        ))

    def get_manga_name(self) -> str:
        re = self.re.search(self.uriRegex, self.get_url())
        self.__lang = re.group(1)
        return re.group(2)

    def get_chapters(self):  # issue #61
        manga_idx = self.re.search(r'.manga_id2\s?=\s?"(.+?)";', self.content).group(1)
        return self.json.loads(self.http_get(self.apiUri.format(
            self.domain,
            'manga',
            manga_idx,
        ))).get('chapters', [])

    def get_files(self):
        items = self.json.loads(self.http_get(self.apiUri.format(
            self.domain,
            'chapter',
            self.chapter[3]
        ))).get('images', [])
        return [self.__cdn_url + i[1] for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('#rightContent .info img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaEdenCom
