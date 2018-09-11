from manga_py.provider import Provider
from .helpers.std import Std


class GoodMangaNet(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(r'/chapter/(\d+)', self.chapter).group(1)

    def get_main_content(self):
        url = self.get_url()
        if ~url.find('/chapter/'):
            url = self.html_fromstring(url, '#manga_head h3 > a', 0).get('href')
        _id = self.re.search(r'net/(\d+/[^/]+)', url).group(1)
        return self.http_get('{}/{}'.format(self.domain, _id))

    def get_manga_name(self) -> str:
        url = self.get_url()
        reg = r'/([^/]+)/chapter/|net/\d+/([^/]+)'
        groups = self.re.search(reg, url).groups()
        return groups[0] if groups[0] else groups[1]

    @staticmethod
    def get_chapters_links(parser):
        return [i.get('href') for i in parser.cssselect('#chapters li > a')]

    def get_chapters(self):
        selector = '#chapters li > a'
        chapters = self._elements(selector)
        pagination = self._elements('.pagination li > button[href]')
        for i in pagination:
            chapters += self._elements(selector, self.http_get(i.get('href')))
        return chapters

    def get_files(self):
        img_selector = '#manga_viewer > a > img'
        parser = self.html_fromstring(self.chapter)
        images = self._images_helper(parser, img_selector)
        pages = self._first_select_options(parser, '#asset_2 select.page_select', True)
        for i in pages:
            _parser = self.html_fromstring(i.get('value'))
            images += self._images_helper(_parser, img_selector)
        return images

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = GoodMangaNet
