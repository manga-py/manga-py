from src.provider import Provider


class MangaFoxMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = '/manga/[^/]+/([^/]+)/'
        chapter = self.get_current_chapter()
        groups = self.re.search(selector, chapter).group(1).split('.')
        idx = [
            groups[0],
            0 if len(groups) < 2 else groups[1]
        ]
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)/?', self.get_url()).group(1)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content(), '#chapters a.tips')
        if not parser:
            return []
        return [i.get('href') for i in parser]

    def prepare_cookies(self):
        pass

    @staticmethod
    def _content2image_url(parser):
        result = parser.cssselect('img#image')
        return result[0].get('src')

    def __get_files_url(self):
        volume = self.get_current_chapter()
        url = self.http().normalize_uri(volume)
        if url.find('.html') > 0:
            url = url[0: url.rfind('/')]
        return url

    def get_files(self):
        _url = self.__get_files_url()
        url = '{}/1.html'.format(_url)
        selector = '#top_bar .r .l select.m option'
        parser = self.html_fromstring(url)
        pages = [i.get('value') for i in parser.cssselect(selector)]

        images = [self._content2image_url(parser)]

        for n in pages:
            if int(n) < 2:
                continue
            url = '{}/{}.html'.format(_url, n)
            parser = self.html_fromstring(url)
            images.append(self._content2image_url(parser))

        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaFoxMe
