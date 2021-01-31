from manga_py.provider import Provider
from manga_py.download_methods import WholeArchiveDownloader
from .helpers.std import Std

class MangaFreakNet(Provider, Std):
    _downloader = WholeArchiveDownloader

    def get_archive_name(self):
        return self.chapter['archive_name']

    def get_chapter_index(self) -> str:
        return self.re.search(r'.+_(\d+)', self.chapter[1]).group(1)

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/Manga/([^?/#]+)')

    def get_chapters(self):
        items = self._elements('.manga_series_list td a[download]')
        return [{'archive_name': i.get('download'), 'download_link': i.get('href')} for i in items][::-1]

    def get_files(self):
        pass

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())

    def get_cover(self) -> str:
        return self._cover_from_content('.manga_series_image img')

    def chapter_for_json(self):
        return self.chapter['download_link']


main = MangaFreakNet
