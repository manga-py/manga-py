from manga_py.provider import Provider
from .helpers.std import Std


class TruyenVnsharingSite(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'_(\d+(?:\.\d+)?)[^\d]?')
        ch = self.chapter
        return '-'.join(re.search(ch).group(1).split('.'))

    def get_content(self):
        name = self._get_name('/read/([^/]+/[^/]+/[^/]+)')
        url = '{}/index/read/{}'
        return self.http_get(url.format(
            self.domain,
            name
        ))

    def get_manga_name(self) -> str:
        return self._get_name('/read/[^/]+/[^/]+/([^/]+)')

    def get_chapters(self):
        return self._elements('#manga-info-list a.title')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.read_content .br_frame > img')

    def get_cover(self) -> str:
        img = self._elements('.info_ava.manga')
        if img and len(img):
            return self.parse_background(img[0])

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TruyenVnsharingSite
