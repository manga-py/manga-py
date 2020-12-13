from manga_py.provider import Provider
from .helpers.std import Std


class WieMangaCom(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name([
            self.chapter_id,
            self.re.search('/chapter/([^/]+)', self.chapter).group(1)
        ])

    def get_chapter_index(self) -> str:
        return self.re.search(r'/chapter/[^/]+/(\d+)/', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga/{}.html')

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/chapter/'):
            url = self.html_fromstring(url, '.sitemaplist a + a', 0).get('href')
            url = self.http().normalize_uri(url)
        return self.re.search(r'/manga/([^/]+)\.html', url).group(1)

    def get_chapters(self):
        return self._elements('.chapterlist .col1 a')

    def get_files(self):
        selector = 'img#comicpic'
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, 'select#page')
        items = self._images_helper(parser, selector)
        for i in pages:
            parser = self.html_fromstring(i.get('value'))
            items += self._images_helper(parser, selector)
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('.bookfrontpage a > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = WieMangaCom
