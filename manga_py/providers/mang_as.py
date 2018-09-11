from manga_py.provider import Provider
from .helpers.std import Std
from sys import stderr


class MangAs(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/[^/]+/([^/]+)', self.chapter).group(1)
        return idx.replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapter-title-rtl > a')

    def get_files(self):
        content = self.http_get(self.chapter)
        self.http().referer = self.chapter
        items = self.re.search(r'var\s+pages\s*=\s*(\[.+\])', content)
        if not items:
            self.log('Images not found!', file=stderr)
            return []
        n = self.http().normalize_uri
        items = self.json.loads(items.group(1))
        return [n(i.get('page_image')) for i in items]

    def prepare_cookies(self):
        self._base_cookies(self.get_url())

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed > img.img-responsive')

    def book_meta(self) -> dict:
        pass


main = MangAs
