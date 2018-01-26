from libs.provider import Provider


class GoodMangaNet(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        return self.re.search('/chapter/(\\d+)', self.get_current_chapter()).group(1)

    def get_main_content(self):
        url = self.get_url()
        if url.find('/chapter/') > 0:
            url = self.html_fromstring(url, '#manga_head h3 > a', 0).get('href')
        _id = self.re.search('net/(\\d+/[^/]+)', url).group(1)
        return self.http_get('{}/{}'.format(self.get_domain(), _id))

    def get_manga_name(self) -> str:
        url = self.get_url()
        reg = '/([^/]+)/chapter/|net/\\d+/([^/]+)'
        groups = self.re.search(reg, url).groups()
        return groups[0] if groups[0] else groups[1]

    @staticmethod
    def get_chapters_links(parser):
        return [i.get('href') for i in parser.cssselect('#chapters li > a')]

    def get_chapters(self):
        content = self.get_main_content()
        if not content:
            return []
        parser = self.document_fromstring(content)
        chapters = self.get_chapters_links(parser)
        pagination = parser.cssselect('.pagination li > button[href]')
        for i in pagination:
            cnt = self.html_fromstring(i.get('href'))
            chapters += self.get_chapters_links(cnt)
        return chapters

    def prepare_cookies(self):
        pass

    @staticmethod
    def __get_image(p):
        img = p.cssselect('#manga_viewer > a > img')
        return img[0].get('src')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        images = [self.__get_image(parser)]
        for i in parser.cssselect('#asset_2 select.page_select option + option'):
            _parser = self.html_fromstring(i.get('value'))
            images.append(self.__get_image(_parser))
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = GoodMangaNet
