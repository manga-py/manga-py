from .gomanga_co import GoMangaCo
from .helpers.std import Std


class KomikIdCom(GoMangaCo, Std):
    _name_re = '/manga/([^/]+)'
    _content_str = '{}/manga/{}'
    _chapters_selector = '.chapter-title-rtl a'

    def get_chapter_index(self) -> str:
        re = r'/manga/[^/]+/(\d+)(?:[^\d](\d+))?'
        idx = self.re.search(re, self.chapter)
        return self._join_groups(idx.groups())

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#all img[data-src]', 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed img')

    def prepare_cookies(self):
        pass


main = KomikIdCom
