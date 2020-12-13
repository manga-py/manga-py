from manga_py.provider import Provider
from .helpers.std import Std


class ReadMangaEu(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/\d+/[^/]+/([^/]+)', self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_content(self):
        name = self._get_name('/(manga/\d+/[^/]+)')
        return self.http_get('{}/{}'.format(self.domain, name))

    def get_manga_name(self) -> str:
        return self._get_name('/manga/\d+/([^/]+)')

    def get_chapters(self):
        selector = '#chapters_b a[href*="/manga/"]'
        return self._elements(selector)

    def parse_files(self, parser):
        images_class = '.mainContent img.ebook_img'
        return self._images_helper(parser, images_class)

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = parser.cssselect('#jumpto > option + option')
        images = self.parse_files(parser)
        for i in pages:
            url = self.http().normalize_uri(i.get('value'))
            parser = self.html_fromstring(url)
            images += self.parse_files(parser)
        return images

    def get_cover(self):
        return self._cover_from_content('.ebook_cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadMangaEu
