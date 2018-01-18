from .provider import Provider


class ComicExtra(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return self._storage['current_chapter']
        # return self.re.search('(\d+)', self.get_current_chapter()).group(1)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/comic/{}'.format(self.get_domain(), name))

    def get_manga_name(self):
        url = self.get_url()
        test = self.re.search('/comic/([^/]+)', url)
        if test:
            return test.group(1)
        return self.re.search('/([^/]+)/chapter', url).group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_main_content(), '#list td a')
        return ['%s/full' % i.get('href') for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '.chapter-container img.chapter_img')
        return [i.get('src') for i in items]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ComicExtra
