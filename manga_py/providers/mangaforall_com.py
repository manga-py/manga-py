from manga_py.provider import Provider
from .helpers.std import Std


class MangaForAllCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}_{}'.format(
            *self._idx_to_x2(idx),
            self.chapter_id
        )

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'-(\d+(?:\.\d+)?)-')
        ch = self.chapter
        return '-'.join(re.search(ch).group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/m/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/m/([^/]+)')

    def get_chapters(self):
        return self._elements('.Chapters ul.list-unstyled > li a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.container ul.list-unstyled > li img')

    def get_cover(self) -> str:
        return self._cover_from_content('meta[property="og:image"]', 'content')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaForAllCom
