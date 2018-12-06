from manga_py.provider import Provider
from .helpers.std import Std


class MangaBoxMe(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.re.search(r'/episodes/(\d+)', self.chapter).group(1)

    def get_main_content(self):
        idx = self._get_name(r'/reader/(\d+)/episodes/')
        return self.http_get('{}/reader/{}/episodes/'.format(self.domain, idx))

    def get_manga_name(self) -> str:
        selector = 'meta[property="og:title"]'
        title = self.document_fromstring(self.content, selector, 0)
        return title.get('content').strip()

    def get_chapters(self):
        selector = '.episodes_list .episodes_item > a'
        return self._elements(selector)

    def get_files(self):
        items = self.html_fromstring(self.chapter, 'ul.slides li > img')
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('.episodes_img_main', 'data-src')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaBoxMe
