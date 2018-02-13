from src.provider import Provider


class MangaTailCom(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}-{}'.format(
            self._chapter_index(),
            self.get_chapter_index()
        )

    def get_chapter_index(self) -> str:  # Oh ...
        idx = self.get_current_chapter()[0]
        re = self.re.search(r'.+\s(\d+(?:\.\d+)?)', idx)
        if re:
            return re.group(1)
        return idx

    def get_main_content(self):
        url = self.get_url()
        if self.__local_storage:
            url = self.__local_storage
        return self.http_get(url)

    def get_manga_name(self) -> str:
        selector = '.main-content-inner .page-header'
        header = self.html_fromstring(self.get_url(), selector, 0)
        link = header.cssselect('a.active + a')
        if link:
            link = self.http().normalize_uri(link.get('href'))
            self.__local_storage = link
            header = self.html_fromstring(link, selector, 0)
        return header.text_content().strip()

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '.chlist td a')
        n = self.http().normalize_uri
        return [(i.text_content().strip(), n(i.get('href'))) for i in items]

    def prepare_cookies(self):
        self._storage['cookies'] = self.http().get_base_cookies(self.get_url()).get_dict()

    def get_files(self):
        url = self.get_current_chapter()[1]
        items = self.html_fromstring('{}{}'.format(url, '?page=all'), '#images img')
        n = self.http().normalize_uri
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:  # TODO
        cover = self.document_fromstring(self.get_storage_content(), 'iframe.authcache-esi-assembly', 0)
        cover = self.json.loads(cover.text_content().strip()).get('field')
        key = cover.keys()[0]
        cover = self.document_fromstring(cover.get(key), '.field-type-image img', 0)
        return self.http().normalize_uri(cover.get('src'))


main = MangaTailCom
