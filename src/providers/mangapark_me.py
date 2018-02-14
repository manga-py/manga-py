from src.provider import Provider


class MangaParkMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/s.+?(?:/v(\d+))?/c(\d+[^/]*)'
        idx = self.re.search(selector, self.get_current_chapter())
        return '{}-{}'.format(
            1 if idx[0] is None else idx[0],
            idx[1]
        )

    def get_main_content(self):
        print('{}/{}'.format(self.get_domain(), self.get_manga_name()));exit()  # FIXME!

        return self.http_get('{}/manga/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), 'div.stream:last-child em a:last-child'
        return self.document_fromstring(c, s)

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '#viewer img.img')
        return [i.get('src') for i in items]


main = MangaParkMe
