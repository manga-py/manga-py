from libs.provider import Provider


class InMangaCom(Provider):

    __local_storage = None

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self.get_current_chapter()['Number'])

    def get_main_content(self):
        if not self.__local_storage.get('uri_hex', False):
            self.get_manga_name()
        url = '{}/chapter/getall?mangaIdentification={}'.format(
            self.get_domain(),
            self.__local_storage['uri_hex']
        )
        data = self.json.loads(self.http_get(url))['data']
        return self.json.loads(data)

    def get_manga_name(self) -> str:
        url = self.get_url()
        test = self.re.search('com/ver/manga/[^/]+/\\d+/[^/]+', url)
        if test:
            content = self.html_fromstring(url, '.chapterControlsContainer label.blue a.blue', 0)
            url = self.get_domain() + content.get('href')
        test = self.re.search('com/ver/manga/([^/]+)/([^/]+)', url)
        groups = test.groups()
        self.__local_storage['manga_name'] = groups[0]
        self.__local_storage['uri_hex'] = groups[1]
        return self.__local_storage['manga_name']

    def get_chapters(self):
        items = self.storage_main_content()['result']
        return items[::-1]

    def prepare_cookies(self):
        self.__local_storage = {}

    def get_files(self):
        chapter = self.get_current_chapter()
        domain = self.get_domain()
        files_url = '{}/page/getPageImage/?identification={}'
        url = '{}/ver/manga/{}/{}/{}'.format(
            domain,
            self.__local_storage['manga_name'],
            chapter['FriendlyChapterNumber'],
            chapter['Identification']
        )
        images = self.html_fromstring(url, '.PagesContainer img.ImageContainer')
        return [files_url.format(domain, i.get('id')) for i in images]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = InMangaCom
