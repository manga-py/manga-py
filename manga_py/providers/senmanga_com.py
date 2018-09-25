from manga_py.provider import Provider
from .helpers.std import Std


class SenMangaCom(Provider, Std):

    def get_chapter_index(self) -> str:
        ch = self.chapter
        re = r'\.com/[^/]+/(\d+)([^/\d][^/]*)?/'
        idx = self.re.search(re, ch).groups()
        fmt = '{}'
        if idx[1]:
            fmt += '-{}'
        return fmt.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self._elements('.list .element > .title > a')[::-1]

    def get_files(self):
        url = self.chapter
        parser = self.html_fromstring(url)
        pages = self._first_select_options(parser, 'select[name="page"]')
        src = parser.cssselect('#picture')[0].get('src')
        images = [src]
        for i in pages:
            images.append(self.re.sub(r'\d+\?token', i.get('value') + '?token', src))
        return images

    def prepare_cookies(self):
        self._base_cookies()

    def get_cover(self) -> str:
        return self._cover_from_content('.thumbnail > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = SenMangaCom
