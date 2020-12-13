from manga_py.provider import Provider
from .helpers.std import Std


class NeuMangaTv(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search(r'/manga/[^/]+/(\d+(?:\+\d+))', chapter).group(1)
        return '-'.join(idx.split('+'))

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('#scans .item-content a')

    def get_files(self):
        img_selector = '.imagechap'
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, '.readnav select.page')
        images = self._images_helper(parser, img_selector)
        for i in pages:
            url = i.get('value').replace('//', '/').replace(':/', '://')
            images += self._images_helper(self.html_fromstring(url), img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.info img.imagemg')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = NeuMangaTv
