from src.provider import Provider


class GoMangaCo(Provider):
    _name_re = '/reader/[^/]+/([^/]+)/'
    _content_str = '{}/reader/series/{}/'
    _chapters_selector = '.list .element .title a'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-', 2)
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        url = self.get_current_chapter()
        index_re = '/rea\\w+/[^/]+/[^/]+/(?:[^/]+/)?(\\d+/\\d+(?:/\\d+)?)'
        group = self.re.search(index_re, url).group(1)
        return group.replace('/', '-')

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get(self._content_str.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search(self._name_re, self.get_url()).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), self._chapters_selector)

    def _get_json_selector(self, content):
        idx = self.re.search('page_width\\s=\\sparseInt\\((\\w+)\\[', content).group(1)
        return 'var\\s{}\\s*=\\s*(\\[.+\\])'.format(idx)

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        selector = self._get_json_selector(content)
        items = self.json.loads(self.re.search(selector, content).group(1))
        return [i.get('url') for i in items]

    def get_cover(self) -> str:
        return self._get_cover_from_content('.thumbnail img')

    def prepare_cookies(self):
        self.cf_protect(self.get_url())


main = GoMangaCo
