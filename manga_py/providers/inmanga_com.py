from manga_py.provider import Provider
from .helpers.std import Std


class InMangaCom(Provider, Std):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self.chapter['Number'])

    def get_main_content(self):
        if not self.__local_storage.get('uri_hex', False):
            self.get_manga_name()
        url = '{}/chapter/getall?mangaIdentification={}'.format(
            self.domain,
            self.__local_storage['uri_hex']
        )
        data = self.json.loads(self.http_get(url))['data']
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

    def get_chapters(self):
        return self.content['result'][::-1]

    def prepare_cookies(self):
        self.__local_storage = {}

    def get_files(self):
        chapter = self.chapter
        domain = self.domain
        files_url = '{}/page/getPageImage/?identification={}'
        url = '{}/ver/manga/{}/{}/{}'.format(
            domain,
            self.manga_name,
            chapter['FriendlyChapterNumber'],
            chapter['Identification']
        )
        images = self.html_fromstring(url, '.PagesContainer img.ImageContainer')
        return [files_url.format(domain, i.get('id')) for i in images]

    def get_cover(self):
        idx = self.__local_storage['uri_hex']
        return '{}/manga/getMangaImage?identification={}'.format(self.domain, idx)


main = InMangaCom
