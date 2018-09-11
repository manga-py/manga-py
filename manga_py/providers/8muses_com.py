from manga_py.provider import Provider
from .helpers import eight_muses_com
from .helpers.std import Std


class EightMusesCom(Provider, Std):
    _chapters = None
    chapter_selector = '.gallery a.c-tile[href^="/comics/"]'
    helper = None
    _images_path = 'image/fl'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/(?:album|picture)/([^/]+/[^/]+(?:/[^/]+)?)')
        ch = self.chapter
        if isinstance(ch, list) and len(ch) > 0:
            ch = ch[0]
        if isinstance(ch, dict):
            ch = ch.get('href')
        idx = re.search(ch).group(1)
        return '-'.join(idx.split('/'))

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/album/([^/]+)')

    def get_chapters(self):
        chapters = self._elements(self.chapter_selector)
        return self.helper.chapters(chapters)

    def _parse_images(self, images) -> list:
        return ['{}/{}/{}'.format(
            self.domain,
            self._images_path,
            i.get('value')
        ) for i in images if i.get('value')]

    @staticmethod
    def _sort(items: dict) -> list:
        items = [items[i] for i in sorted(items, key=lambda x: int(x)) if len(items[i]) > 5]
        return list(set(items))

    def get_files(self):
        images = {}
        _n = self.http().normalize_uri
        for n, i in enumerate(self.chapter):
            if n % 4 < 2:
                img = self.html_fromstring(_n(i.get('href')), '#imageName,#imageNextName')
                images[str(n)] = img[0]
                images[str(n + 2)] = img[1]
        return self._parse_images(self._sort(images))

    def get_cover(self) -> str:
        pass

    def prepare_cookies(self):
        self._chapters = []
        self._base_cookies()
        self.helper = eight_muses_com.EightMusesCom(self)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = EightMusesCom
