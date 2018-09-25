from manga_py.provider import Provider
from .helpers.std import Std


class PuzzmosCom(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search('/manga/[^/]+/([^/]+)', chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('#bolumler td:first-child a')

    def get_files(self):
        img_selector = '.chapter-content img.chapter-img'
        url = self.chapter
        parser = self.html_fromstring(url)
        pages = parser.cssselect('.col-md-12 > .text-center > select option + option')
        images = self._images_helper(parser, img_selector)
        for i in pages:
            parser = self.html_fromstring(i.get('value'))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('img.thumbnail.manga-cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = PuzzmosCom
