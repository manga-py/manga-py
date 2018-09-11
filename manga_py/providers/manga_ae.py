from manga_py.provider import Provider
from .helpers.std import Std


class MangaAe(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.ae/[^/]+/(\d+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.ae/([^/]+)')

    def get_chapters(self):
        return self._elements('li > a.chapter')

    def get_files(self):
        img_selector = '#showchaptercontainer img'
        parser = self.html_fromstring(self.chapter)
        pages = parser.cssselect('#morepages a + a')
        images = self._images_helper(parser, img_selector)
        if pages:
            for i in pages:
                parser = self.html_fromstring(i.get('href'))
                images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('img.manga-cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaAe
