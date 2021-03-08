from manga_py.provider import Provider
from .helpers.std import Std


class InMangaCom(Provider, Std):
    __local_storage = None

    def get_chapter_index(self) -> str:
        return str(self.chapter['Number'])

    def get_content(self):
        if not self.__local_storage.get('uri_hex', False):
            self.get_manga_name()
        url = '{}/chapter/getall?mangaIdentification={}'.format(
            self.domain,
            self.__local_storage['uri_hex']
        )
        with self.http().get(url) as resp:
            data = resp.json()['data']

        return self.json.loads(data)

    def get_manga_name(self) -> str:
        url = self.get_url()
        test = self.re.search(r'/ver/manga/[^/]+/\d+/[^/]+', url)
        if test:
            content = self._elements('.chapterControlsContainer label.blue a.blue')[0]
            url = self.domain + content.get('href')
        manga_name, uri_hex = self.re.search('/ver/manga/([^/]+)/([^/]+)', url).groups()
        self.__local_storage['manga_name'] = manga_name
        self.__local_storage['uri_hex'] = uri_hex
        return self.__local_storage['manga_name']

    @staticmethod
    def __sort_chapters(items, reverse=False):
        return sorted(items, key=lambda i: float(i['FriendlyChapterNumber']), reverse=reverse)

    def get_chapters(self):
        items = self.content['result']
        return self.__sort_chapters(items, True)

    def prepare_cookies(self):
        self.__local_storage = {}

    def _make_url(self, chapter):
        return '{}/ver/manga/{}/{}/{}'.format(
            self.domain,
            self.manga_name,
            chapter['FriendlyChapterNumber'],
            chapter['Identification']
        )

    def get_files(self):
        files_url = '{}/page/getPageImage/?identification={}'
        url = self._make_url(self.chapter)
        images = self.html_fromstring(url, '.PagesContainer img.ImageContainer')

        domain = self.domain
        return [files_url.format(domain, i.get('id')) for i in images]

    def get_cover(self):
        idx = self.__local_storage['uri_hex']
        return '{}/manga/getMangaImage?identification={}'.format(self.domain, idx)

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self._make_url(self.chapter)


main = InMangaCom
