from manga_py.provider import Provider
from .helpers.std import Std


class MangakuWebId(Provider, Std):

    def get_archive_name(self) -> str:
        ch = self.chapter
        return self.normal_arc_name({'vol': [
            self.chapter_id,
            self.re.search(':[^/]+/([^/]+)', ch).group(1)
        ]})

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name(r'\.id/([^/]+)')

    def get_chapters(self):
        return self._elements('div[style] a[target]')

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self._elements('.entry .separator > a > img', content)
        return [i.get('src') for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('span > small img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangakuWebId
