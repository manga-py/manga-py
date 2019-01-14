from manga_py.provider import Provider
from .helpers.std import Std


class MerakiScansCom(Provider, Std):
    _content_url = '{}/details/{}/'

    def get_chapter_index(self) -> str:
        re = self.re.compile('com/[^/]+/([^/]+)')
        idx = re.search(self.chapter).group(1)
        return '-'.join(idx.split('.'))

    def _home_url(self):
        return self._content_url.format(self.domain, self.manga_name)

    def get_main_content(self):
        return self.http_get(self._home_url())

    def get_manga_name(self) -> str:
        return self._get_name('com/details/([^/]+)')

    def get_chapters(self):
        selector = '.clickable-chapter'
        items = self._elements(selector)
        return [i.get('data-href') for i in items]

    def get_files(self):
        content = self.http_get(self.chapter)
        slug = self.re.search(r'manga_slug\s*=\s*[\'"](.+)[\'"]', content).group(1)
        chapter = self.re.search(r'viewschapter\s*=\s*[\'"](.+)[\'"]', content).group(1)
        images = self.re.search(r'images\s*=\s*(\[.+\])', content).group(1).replace('\'', '"')
        images = self.json.loads(images)

        # SRC RULE: "/manga/" + manga_slug + "/" + currentChapter + "/" + images[pageNum - 1];

        return ['{}/manga/{}/{}/{}'.format(self.domain, slug, chapter, i) for i in images]

    def get_cover(self) -> str:
        return self._cover_from_content('#cover_img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def prepare_cookies(self):
        self.http().cookies['reading_type'] = 'long'


main = MerakiScansCom
