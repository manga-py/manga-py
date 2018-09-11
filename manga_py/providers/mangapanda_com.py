from manga_py.provider import Provider
from .helpers.std import Std


class MangaPandaCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.com/[^/]+/([^/]+)', self.chapter)
        return idx.group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self._elements('#listing a')

    def get_files(self):
        img_selector = '#imgholder img'
        url = self.http().normalize_uri(self.chapter)

        parser = self.html_fromstring(url, '#container', 0)
        count_pages = self._first_select_options(parser, '#selectpage')
        images = self._images_helper(parser, img_selector)

        n = 1
        while n < len(count_pages):
            parser = self.html_fromstring('{}/{}'.format(url, 1 + n))
            images += self._images_helper(parser, img_selector)
            n += 1

        return images

    def get_cover(self):
        return self._cover_from_content('#mangaimg img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaPandaCom
