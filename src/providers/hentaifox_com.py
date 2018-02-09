from src.provider import Provider


class HentaiFoxCom(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        return 'archive'

    def get_main_content(self):
        if self.__local_storage is None:
            idx = self.re.search('/g(?:allery)?/(\\d+)', self.get_url())
            url = '{}/gallery/{}/'.format(self.get_domain(), idx)
            self.__local_storage = self.http_get(url)
        return self.__local_storage

    def get_manga_name(self) -> str:
        content = self.get_main_content()
        h1 = self.document_fromstring(content, '.info h1', 0)
        return h1.text_content().strip()

    def get_chapters(self):
        return [b'']

    def get_files(self):
        c, s = self.get_storage_content(), '.gallery .preview_thumb a'
        pages = self.document_fromstring(c, s)
        items = []
        n = self.http().normalize_uri
        for i in pages:
            url = self.html_fromstring(n(i.get('href')), '#gimg').get('src')
            items.append(n(url))
        return items

    def get_cover(self) -> str:
        return self._get_cover_from_content('.cover img')


main = HentaiFoxCom
