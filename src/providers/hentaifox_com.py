from src.provider import Provider


class HentaiFoxCom(Provider):
    __local_storage = None
    _idx_re = r'/g(?:allery)?/(\d+)'
    _url_str = '{}/gallery/{}/'
    _name_re = '.info h1'

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        return 'archive'

    def get_main_content(self):
        if self.__local_storage is None:
            idx = self.re.search(self._idx_re, self.get_url())
            url = self._url_str.format(self.get_domain(), idx)
            self.__local_storage = self.http_get(url)
        return self.__local_storage

    def get_manga_name(self) -> str:
        content = self.get_main_content()
        text = self.document_fromstring(content, self._name_re, 0)
        return text.text_content().strip()

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
