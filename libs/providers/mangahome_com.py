from libs.provider import Provider


class MangaHomeCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = '/manga/[^/]+/[^\\d]+(\\d+)(?:\\.(\\d+))?'
        groups = self.re.search(selector, self.get_current_chapter()).groups()
        idx = [
            groups[0],
            0 if groups[1] is None else groups[1]
        ]
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_main_content(), '.detail-chlist a')
        return [i.get('href') for i in parser]

    def prepare_cookies(self):
        pass

    @staticmethod
    def _content2image_url(parser):
        return parser.cssselect('img#image')[0].get('src')

    def get_files(self):
        _url = self.http().normalize_uri(self.get_current_chapter())
        parser = self.html_fromstring(_url)
        pages_selector = '.mangaread-top .mangaread-pagenav select option + option'
        pages = [i.get('value') for i in parser.cssselect(pages_selector)]

        images = [self._content2image_url(parser)]

        for i in pages:
            url = self.http().normalize_uri(i)
            images.append(self._content2image_url(self.html_fromstring(url)))

        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaHomeCom
