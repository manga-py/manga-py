from manga_py.provider import Provider
from .helpers.std import Std


class MangaHomeCom(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/[^\d]+(\d+)(?:\.(\d+))?'
        idx = self.re.search(selector, self.chapter).groups()
        return self._join_groups(idx)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail-chlist a')

    def get_files(self):
        n = self.http().normalize_uri
        img_selector = 'img#image'
        _url = n(self.chapter)
        parser = self.html_fromstring(_url)
        p_selector = '.mangaread-top .mangaread-pagenav select'
        pages = self._first_select_options(parser, p_selector)
        images = self._images_helper(parser, img_selector)
        for i in pages:
            parser = self.html_fromstring(n(i.get('value')))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self):
        return self._cover_from_content('.detail-cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHomeCom
