from src.provider import Provider


class MangaClubRu(Provider):

    local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/view/[^/]+/v(\\d+)-c(\\d+).html').groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        if not self.local_storage:
            self.get_manga_name()
        return self.http_get('{}/{}.html'.format(self.get_domain(), self.local_storage[0]))

    def get_manga_name(self) -> str:
        selector = '\\.ru(?:/manga/view)?/(?:(\\d+\\-.+)/(.+)\\.html)'
        html = self.re.search(selector, self.get_url())
        self.local_storage = html.groups()
        return self.local_storage[1]

    def get_chapters(self):
        selector = '.manga-ch-list-item > a[href^="http"]'
        parser = self.document_fromstring(self.get_storage_content(), selector)
        return [i.get('href') for i in parser]

    def get_files(self):
        result = self.html_fromstring(self.get_current_chapter(), '.manga-lines-page a.manga-lines')
        return [i.get('data-i') for i in result]


main = MangaClubRu
