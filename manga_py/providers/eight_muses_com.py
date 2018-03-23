from manga_py.provider import Provider
from .helpers.std import Std
from .helpers import eight_muses_com


class EightMusesCom(Provider, Std):
    chapter_selector = '.gallery a.c-tile[href^="/comics/"]'
    helper = None
    _images_path = 'image/fl'

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/album/([^/]+/[^/]+(?:/[^/]+)?)')
        idx = re.search(self.chapter).group(1)
        return '-'.join(idx.split('/'))

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/album/([^/]+)')

    def get_chapters(self):
        chapters = self._elements(self.chapter_selector)
        return self.helper.chapters(chapters)

    def _parse_images(self, images) -> list:
        return ['{}/{}/{}'.format(self.domain, self._images_path, i.get('value')) for i in images]

    def get_files(self):
        images = []
        _n = self.http().normalize_uri
        for n, i in enumerate(self.chapter):
            if n % 2 == 0:
                images += self.html_fromstring(_n(i.get('href')), '#imageName,#imageNextName')
        return self._parse_images(images)

    def get_cover(self) -> str:
        pass

    def prepare_cookies(self):
        self._base_cookies()
        self.helper = eight_muses_com.EightMusesCom(self)


main = EightMusesCom
