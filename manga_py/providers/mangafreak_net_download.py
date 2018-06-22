from manga_py.provider import Provider
from .helpers.std import Std, Http2


class MangaFreakNet(Provider, Std):

    def get_archive_name(self):
        return self.chapter[0]

    def get_chapter_index(self) -> str:
        return self.re.search(r'.+_(\d+)', self.chapter[1]).group(1)

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/Manga/([^?/#]+)')

    def get_chapters(self):
        items = self._elements('.manga_series_list td a[download]')
        return [(i.get('download'), i.get('href')) for i in items]

    def loop_chapters(self):
        items = self._storage['chapters'][::-1]
        Http2(self).download_archives([i[1] for i in items])

    def get_files(self):
        pass

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_cover(self) -> str:
        return self._cover_from_content('.manga_series_image img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter[1]


main = MangaFreakNet
