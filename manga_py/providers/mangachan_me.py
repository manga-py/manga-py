from manga_py.provider import Provider
from .helpers.std import Std


class MangaChanMe(Provider, Std):
    _full_name_selector = r'/(?:online|manga|related)/(\d+-.+\.html)'
    _idx_selector = r'/(?:online|manga|related)/(\d+)-'

    def get_chapter_index(self) -> str:
        name = self.chapter
        idx = self.re.search(r'_v(\d+)_ch(\d+)', name).groups()
        return '{}-{}'.format(*idx)

    def get_content(self):
        pass

    def _online_(self, url):
        if self.re.search(r'/online/\d+', url):
            content = self.http_get(url)
            url = self.re.search(r'content_id.+?(/manga/.+\.html)', content).group(1)
        return url

    def get_manga_name(self) -> str:
        _name_selector = r'/(?:online|manga|related)/\d+-(.+)\.html'
        url = self._online_(self.get_url())
        return self.re.search(_name_selector, url).group(1)

    def get_chapters(self):
        url = self._online_(self.get_url())
        url = '{}/manga/{}'.format(
            self.domain,
            self.re.search(self._full_name_selector, url).group(1)
        )
        return self.html_fromstring(url, '.table_cha .manga a')

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self.re.search(r'"?fullimg"?\s?:\s?(\[.+\])', content).group(1)
        images = self.json.loads(items.replace('",]', '"]'))  # patch
        return images

    def get_cover(self):
        selector = r'\.\w{2,7}/[^/]+/(\d+-.+\.html)'
        url = '{}/manga/{}'.format(self.domain, self._get_name(selector))
        img = self._elements('#cover', self.http_get(url))
        if img and len(img):
            return img[0].get('src')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaChanMe
