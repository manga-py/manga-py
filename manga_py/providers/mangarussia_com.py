from urllib.parse import unquote, quote

from manga_py.provider import Provider
from .helpers.std import Std


class MangaRussiaCom(Provider, Std):

    @staticmethod
    def path_url(url):
        return quote(unquote(url)).replace('%3A//', '://')

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        result = self.re.search(r'\+(\d+)\+-\+(\d+)', chapter)
        return '-'.join(result.groups())

    def get_content(self):
        url = '{}/manga/{}.html'.format(self.domain, quote(self.manga_name))
        self._storage['referer'] = self.path_url(self.get_url())
        return self.http_get(url)

    def __name(self, url):
        return self.re.search(r'/manga/(.+)\.html', url).group(1)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if self.re.search('/manga/', url):
            name = self.__name(url)
        else:
            url = self.html_fromstring(url, '.sitemaplist .red', 0).get('href')
            name = self.__name(url)
        return unquote(name)

    def get_chapters(self):
        return self._elements('.chapterlist .col1 a')

    def _get_img(self, parser):
        img = parser.cssselect('img#comicpic')[0]
        urls = [img.get('src')]
        onload = img.get('onload')
        if ~onload and onload.find('(\''):
            urls.append(self.re.search('\(\'(.+)\'\)', onload).group(1))
        return urls

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        result = parser.cssselect('select#page option + option')
        images = self._get_img(parser)
        for n, i in enumerate(result):
            if n and n % 2:
                parser = self.html_fromstring(i.get('value'))
                images += self._get_img(parser)
        return images

    def get_cover(self):
        self._cover_from_content('.bookfrontpage > a > img')

    def before_download_chapter(self):
        self._storage['referer'] = self.path_url(self.chapter)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaRussiaCom
