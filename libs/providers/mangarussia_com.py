from urllib.parse import unquote, quote

from libs.provider import Provider


class MangaRussiaCom(Provider):

    @staticmethod
    def path_url(url):
        return quote(unquote(url)).replace('%3A//', '://')

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        result = self.re_search('\\+(\\d+)\\+\\-\\+(\\d+)', chapter).groups()
        return '{}-{}'.format(*result)

    def get_main_content(self):
        name = self._storage.get('manga_name', self.get_manga_name())
        url = '{}/manga/{}.html'.format(self.get_domain(), quote(name))
        self._storage['referer'] = self.path_url(self.get_url())
        return self.http_get(url)

    def __name(self, url):
        return self.re_search('/manga/(.+)\\.html', url).group(1)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if self.re_search('/manga/', url):
            name = self.__name(url)
        else:
            url = self.html_fromstring(url, '.sitemaplist .red', 0).get('href')
            name = self.__name(url)
        return unquote(name)

    def get_chapters(self):
        content = self.get_storage_content()
        parser = self.document_fromstring(content, '.chapterlist .col1 a')
        urls = [i.get('href') for i in parser]
        return urls

    def prepare_cookies(self):
        pass

    def _get_img(self, parser):
        img = parser.cssselect('img#comicpic')[0]
        urls = [img.get('src')]
        onload = img.get('onload')
        if onload and onload.find('(\'') > 0:
            urls.append(self.re_search('\(\'(.+)\'\)', onload).group(1))
        return urls

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        result = parser.cssselect('select#page option + option')
        images = self._get_img(parser)
        for n, i in enumerate(result):
            if n and n % 2:
                parser = self.html_fromstring(i.get('value'))
                images += self._get_img(parser)
        return images

    def _loop_callback_chapters(self):
        self._storage['referer'] = self.path_url(self.get_current_chapter())

    def _loop_callback_files(self):
        pass


main = MangaRussiaCom
