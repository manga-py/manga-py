from src.provider import Provider
from .helpers.std import Std
from .helpers.e_hentai_org import EHentaiOrg


class TruyenVnsharingSite(Provider, Std):
    pb = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}'
        return fmt.format(*idx)

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'_(\d+(?:\.\d+)?)[^\d]?')
        ch = self.get_current_chapter()
        return '-'.join(re.search(ch).group(1).split('.'))

    def get_main_content(self):
        name = self._get_name('/read/([^/]+/[^/]+/[^/]+)')
        url = '{}/index/read/{}'
        return self.http_get(url.format(
            self.get_domain(),
            name
        ))

    def get_manga_name(self) -> str:
        return self._get_name('/read/[^/]+/[^/]+/([^/]+)')

    def get_chapters(self):
        return self._elements('#manga-info-list a.title')

    def prepare_cookies(self):
        e_h = EHentaiOrg(self)
        self.pb = e_h.parse_background

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        return self._images_helper(parser, '.read_content .br_frame > img')

    def get_cover(self) -> str:
        img = self._elements('.info_ava.manga')
        if img and len(img):
            return self.pb(img[0])


main = TruyenVnsharingSite
