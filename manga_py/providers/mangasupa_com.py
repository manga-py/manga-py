from manga_py.provider import Provider
from .helpers.std import Std


class MangaSupaCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter_([^/]+)', self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        selector = r'\.com/(?:manga|chapter)/([^/]+)'
        return self._get_name(selector)

    def get_chapters(self):
        return self._elements('.chapter-list .row a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.vung_doc img')

    def get_cover(self):
        return self._cover_from_content('.info_image img')


main = MangaSupaCom
