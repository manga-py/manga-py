from .gomanga_co import GoMangaCo


class ReadYagamiMe(GoMangaCo):
    _name_re = '/read/[^/]+/([^/]+)/'
    _content_str = '{}/series/{}/'
    _chapter_re = r'/rea\w+/[^/]+/(?:[^/]+/)?(\d+/\d+(?:/\d+)?)'

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        e = self._elements('h1.title')[0]
        return e.text.strip()

    def get_files(self):
        try:
            return super().get_files()
        except AttributeError:
            # web manga
            parser = self.document_fromstring(self._go_chapter_content)
            return self._images_helper(parser, '.web_pictures > img')

    def _get_json_selector(self, content):
        return r'pages\s*=\s*(\[.+?\])'

    def prepare_cookies(self):
        response = self.http().requests(method='post', data={'adult': 'true'}, url=self.get_url())
        cookies = response.cookies.items()
        for i in cookies:
            self._storage['cookies'][i[0]] = i[1]


main = ReadYagamiMe
