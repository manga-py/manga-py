from src.provider import Provider


class MangaBoxMe(Provider):

    _local_storage = None

    def _prepare_storage(self):
        if not self._local_storage:
            self._local_storage = {}

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return self.re.search(r'/episodes/(\d+)', self.get_current_chapter()).group(1)

    def get_main_content(self):
        if not self._local_storage.get('content', False):
            idx = self.re.search(r'/reader/(\d+)/episodes/', self.get_url()).group(1)
            content = self.http_get('{}/reader/{}/episodes/'.format(self.get_domain(), idx))
            self._local_storage['content'] = content
        return self._local_storage['content']

    def get_manga_name(self) -> str:
        if not self._local_storage.get('content', False):
            self.get_storage_content()
        content = self._local_storage['content']
        selector = 'meta[property="og:title"]'
        title = self.document_fromstring(content, selector, 0)
        return title.get('content')

    def get_chapters(self):
        content = self._local_storage['content']
        selector = '.episodes_list .episodes_item > a'
        return self.document_fromstring(content, selector)

    def prepare_cookies(self):
        self._prepare_storage()

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), 'ul.slides li > img')
        return [i.get('src') for i in items]


main = MangaBoxMe
