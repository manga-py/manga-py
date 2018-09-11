from manga_py.provider import Provider
from .helpers.std import Std


class MangaMewCom(Provider, Std):
    _type = 'manga'

    def get_chapter_index(self) -> str:
        re = r'%s/[^/]+/.+?-(\d+(?:-\d+)?)-\d+' % self._type
        return self.re.search(re, self.chapter).group(1)

    def get_main_content(self):
        url = self.get_url()
        if url.find('/' + self._type + '/') == -1:  # not found
            a = self.html_fromstring(url, 'h1.name a', 0)
            url = a.get('href')
        return self.http_get(url)

    def get_manga_name(self) -> str:
        content = self.http_get(self.get_url())
        return self.text_content(content, 'h1.name a,h1.title')

    def get_chapters(self):
        return self._elements('.chapter .item a')[::-1]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#content .item > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.images img')

    def book_meta(self) -> dict:
        pass


main = MangaMewCom
