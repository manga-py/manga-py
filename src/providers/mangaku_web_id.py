from src.provider import Provider
from .helpers.std import Std


class MangakuWebId(Provider, Std):

    def get_archive_name(self) -> str:
        ch = self.get_current_chapter()
        return 'vol_{:0>3}-{}'.format(
            self._chapter_index(),
            self.re.search(':[^/]+/([^/]+)', ch).group(1)
        )

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self.http_get(self.get_url())

    def get_chapters(self):
        return self._elements('td > small > div a[target]')

    def get_files(self):
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('span > small img')


main = MangakuWebId
