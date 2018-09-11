from manga_py.provider import Provider
from .helpers.std import Std


class MangaReaderNet(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        return self.re.search(r'\.net/[^/]+/([^/]+)', chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.net/([^/]+)')

    def get_chapters(self):
        return self._elements('#listing a')[::-1]

    @staticmethod
    def _get_img(parser):
        return [i.get('src') for i in parser.cssselect('#img')]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, 'select#pageMenu')
        images = self._get_img(parser)
        for i in pages:
            parser = self.html_fromstring(self.domain + i.get('value'))
            images += self._get_img(parser)
        return images

    def get_cover(self):
        return self._cover_from_content('#mangaimg img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaReaderNet
