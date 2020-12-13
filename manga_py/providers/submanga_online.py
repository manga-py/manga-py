from manga_py.provider import Provider
from .helpers.std import Std


class SubMangaOnline(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.capitulos-list td > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#all img.img-responsive', 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('.list-group-item .img-responsive')

    def book_meta(self) -> dict:
        return {
            'author': self.text_content(self.content, '.manga .col-sm-8 h5 + h5'),
            'title': self.text_content(self.content, '.manga .col-sm-8 > h2'),
            'annotation': self.text_content(self.content, '.manga .col-sm-8 h5 + .clear20 + div'),
            'keywords': None,
            'cover': self.get_cover(),
            'rating': None,
        }


main = SubMangaOnline
