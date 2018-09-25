from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicBooksOnlineOrg(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/manga/[^/]+/[^/]+[-_](\d+(?:\.\d+)?)', self.chapter)
        return idx.group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('#mangachapterlist .chapter > a')

    def _get_image(self, parser):
        src = parser.cssselect('a > img.mangapic')
        if not src:
            return None
        return '{}/reader/{}'.format(self.domain, src[0].get('src'))

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.mangapic')

    def get_cover(self):
        self._cover_from_content(self.content, '.field-item > a > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadComicBooksOnlineOrg
