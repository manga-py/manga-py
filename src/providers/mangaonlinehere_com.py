from src.provider import Provider


class MangaOnlineHereCom(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'/read-online/[^/]+?(\d+)(?:.(\d+))?'
        idx = self.re.search(selector, self.get_current_chapter())
        return '{}-{}'.format(
            idx[0],
            0 if idx[1] is None else idx[1]
        )

    def get_main_content(self):
        return self.http_get('{}/manga-info/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        if not self.__local_storage.get('name', None):
            url = self.get_url()
            if self.re.search(r'/read-online/', url):
                url = self.html_fromstring(url, '.back-info a', 0).get('href')
            name = self.re.search('/manga-info/Fuuka', url).group(1)
            self.__local_storage['name'] = name
        return self.__local_storage['name']

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '.list-chapter a')

    def prepare_cookies(self):
        self.__local_storage = {}

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '#list-img img')
        return [i.get('src') for i in items]


main = MangaOnlineHereCom
