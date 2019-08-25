from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt.base_lib import BaseLib


class MangaHereCc(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        selector = r'/manga/[^/]+/[^\d]+(\d+)/[^\d]+(\d+)'
        idx = self.re.search(selector, chapter)
        if idx:
            return '-'.join(idx.groups())
        selector = r'/manga/[^/]+/[^\d]+(\d+)'
        return self.re.search(selector, chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail-main-list a')

    def get_files(self):
        n = self.http().normalize_uri
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content)
        pages = parser.cssselect('.pager-list-left span span + a')[0].get('data-page')
        chapter_id = self.re.search(r'chapterid\s*=\s*(\d+)', content).group(1)
        skip = 0
        images = []
        url = self.re.search(r'(.+/)', self.chapter).group(1)
        for page in range(1, int(pages) + 1):
            if skip > 0:
                skip -= 1
                continue
            js = self.http_get('{}chapterfun.ashx?cid={}&page={}&key={}'.format(url, chapter_id, page, ''))
            result = BaseLib.exec_js('m = ' + self.re.search(r'eval\((.+)\)', js).group(1), 'm')
            img = BaseLib.exec_js(result, 'd')
            skip = len(img) - 1
            images += img
        return [n(i) for i in images]

    def get_cover(self):
        return self._cover_from_content('.detail-info-cover-img')

    def prepare_cookies(self):
        self._base_cookies()
        self.http().cookies['isAdult'] = '1'


main = MangaHereCc
