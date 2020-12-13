from manga_py.provider import Provider
from .helpers.std import Std
from requests import get


class MangaNelosCom(Provider, Std):
    def get_chapter_index(self) -> str:
        ch = self.re.search(r'-chapter-(\d+(?:\.\d+)?)', self.chapter)
        return ch.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.content .chapter a')

    def get_files(self):
        content = self.text_content(self.http_get(self.chapter), '#arraydata')
        images = content.split(',')

        if len(images) == 0:
            return []

        if self._download_cookies is None:
            with get(images[0], stream=True) as req:
                self._download_cookies = req.cookies

        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.media-left.cover-detail')

    def prepare_cookies(self):
        self.http()._download = self._download


main = MangaNelosCom
