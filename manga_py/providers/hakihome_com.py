from manga_py.provider import Provider
from .helpers.std import Std


class HakiHomeCom(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = '.+/([^/]+)/'
        idx = self.re.search(selector, self.chapter)
        return idx.group(1)

    def get_main_content(self):
        selector = r'(https?://[^/]+/[^/]+/[^/]+-\d+/)'
        url = self.re.search(selector, self.get_url())
        return self.http_get(url.group(1))

    def get_manga_name(self) -> str:
        url = self.get_url()
        selector = r'\.com/[^/]+/(.+?)-\d+/'
        return self.re.search(selector, url).group(1)

    def get_chapters(self):
        return self._elements('.listing a.readchap')

    def get_files(self):
        img_selector = '#con img'
        n = self.http().normalize_uri
        uri = n(self.chapter)
        parser = self.html_fromstring(uri, '#contentchap', 0)
        pages = self._first_select_options(parser, '#botn span > select[onchange]')
        images = self._images_helper(parser, img_selector)

        for i in pages:
            parser = self.html_fromstring(n(i.get('value')), '#contentchap', 0)
            images += self._images_helper(parser, img_selector)

        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.noidung img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = HakiHomeCom
