from manga_py.provider import Provider
from .helpers.std import Std


class NiAddCom(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chapter/.*?_(\d+(?:_\d+)?)/')
        return re.search(self.chapter).group(1).replace('_', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail-chlist > a')

    def get_files(self):
        img_selector = 'img.manga_pic'
        url = self.chapter + '-10-{}.html'
        parser = self.html_fromstring(url.format(1))
        pages = len(self._first_select_options(parser, '.sl-page')) + 1
        images = self._images_helper(parser, img_selector)
        for p in range(2, pages):
            parser = self.html_fromstring(url.format(p))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-detailtop img')

    def book_meta(self) -> dict:
        pass


main = NiAddCom
