from manga_py.provider import Provider
from .helpers.std import Std


class FunMangaCom(Provider, Std):

    def _get_chapter_idx(self):
        re = self.re.compile(r'\.com/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_chapter_index(self) -> str:
        return self._get_chapter_idx().replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        items = self._elements('.chapter-list li > a')
        return [i.get('href') + '/all-pages' for i in items]

    def get_files(self):
        items = self.html_fromstring(self.chapter, '.content-inner > img.img-responsive')
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('img.img-responsive.mobile-img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = FunMangaCom
