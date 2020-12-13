from urllib.parse import unquote_plus

from manga_py.provider import Provider
from .helpers.std import Std


class MangaXNet(Provider, Std):
    __name = None

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'\.\w{2,7}/\w/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_content(self):
        url = '{}/m/{}'.format(
            self.domain,
            self.__name,
        )
        return self.http_get(url)

    def get_manga_name(self) -> str:
        self.__name = self._get_name(r'\.\w{2,7}/\w/([^/]+)')
        return unquote_plus(self.__name)

    def get_chapters(self):
        return self._elements('.chlist li a')

    def get_files(self):
        ch = self.re.sub(r'(\.\w{2,7})/\w/', r'\1/f/', self.chapter)
        parser = self.html_fromstring(ch)
        return self._images_helper(parser, 'img.center-block')

    def get_cover(self) -> str:
        return self._cover_from_content('.thumbnail > img')

    def book_meta(self) -> dict:
        pass


main = MangaXNet
