from libs.provider import Provider


class MangaReaderNet(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        return '{}-0'.format(self.re_search('\\.net/[^/]+/([^/]+)', chapter).group(1))

    def get_main_content(self):
        return self.http_get('{}/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re_search('\\.net/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        result = self.document_fromstring(self.get_storage_content(), '#listing a')
        domain = self.get_domain()
        return [domain + i.get('href') for i in result[::-1]]

    def prepare_cookies(self):
        pass

    @staticmethod
    def _get_img(parser):
        return parser.cssselect('#img')[0].get('src')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        result = parser.cssselect('select#pageMenu option + option')
        images = [self._get_img(parser)]
        for i in result:
            parser = self.html_fromstring(self.get_domain() + i.get('value'))
            images.append(self._get_img(parser))
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaReaderNet
