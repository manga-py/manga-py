from manga_py.provider import Provider
from .helpers.std import Std


class MangaSupaCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter_([^/]+)', self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        selector = r'\.\w{2,7}/(?:manga|chapter)/([^/]+)'
        return self._get_name(selector)

    def get_chapters(self):
        return self._elements('.chapter-list .row a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.vung_doc img')

    def get_cover(self):
        return self._cover_from_content('.info_image img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaSupaCom
