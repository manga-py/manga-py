from src.provider import Provider


class WMangaRu(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = '/manga_chapter/[^/]+/(\\d+)/(\\d+)'
        print(self.get_current_chapter())
        idx = self.re.search(selector, self.get_current_chapter()).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        domain, name = self.get_domain(), self.get_manga_name()
        return self.http_get('{}/starter/manga_byid/{}'.format(domain, name))

    def get_manga_name(self) -> str:
        return self.re.search('/starter/manga_[^/]+/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), 'td div div div td > a'
        return self.document_fromstring(c, s)[::-1]

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter(), 'td a.gallery')
        return [i.get('href') for i in parser]


main = WMangaRu
