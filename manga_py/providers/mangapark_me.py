from manga_py.provider import Provider
from .helpers.std import Std


class MangaParkMe(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/s.+?(?:/v(\d+))?/c(\d+[^/]*)'
        idx = self.re.search(selector, self.chapter).groups()
        if idx[0] is None:
            return '0-' + idx[1]
        return '-'.join(idx)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('#list a.ch')

    def get_files(self):
        content = self.http_get(self.chapter)
        data = self.re.search(r'var\simages\s?=\s?(\[.+\])', content)
        if not data:
            return []
        return self.json.loads(data.group(1))

    def get_cover(self):
        return self._cover_from_content('.cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaParkMe
