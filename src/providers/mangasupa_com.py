from src.provider import Provider


class MangaSupaCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter_([^/]+)', self.get_current_chapter())
        idx = idx.group(1).split('.')
        return '{}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        selector = r'\.com/(?:manga|chapter)/([^/]+)'
        return self.re.search(selector, self.get_url()).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '.chapter-list .row a')

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '.vung_doc img')
        return [i.get('src') for i in items]


main = MangaSupaCom
