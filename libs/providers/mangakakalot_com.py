from libs.provider import Provider


class MangaKakalotCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re_search('/chapter_([^/]+)', self.get_current_chapter()).split('.')
        return '{}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re_search('/(?:manga|chapter)/([^/]+)/?', self.get_url())

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '.chapter-list span a')
        return [i.get('href') for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        result = self.html_fromstring(self.get_current_chapter(), '#vungdoc img')
        return [i.get('src') for i in result]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaKakalotCom
