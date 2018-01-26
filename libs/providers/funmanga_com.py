from libs.provider import Provider


class FunMangaCom(Provider):

    def _get_chapter_idx(self):
        return self.re.search('\\.com/[^/]+/([^/]+)', self.get_current_chapter()).group(1)

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._get_chapter_idx())

    def get_chapter_index(self) -> str:
        return self._get_chapter_idx().replace('.', '-')

    def get_main_content(self):
        return self.http_get('{}/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search('\\.com/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_main_content(), '.chapter-list li > a')
        return [i.get('href') + '/all-pages' for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '.content-inner > img.img-responsive')
        return [i.get('src') for i in items]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = FunMangaCom
