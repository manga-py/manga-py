from manga_py.provider import Provider
from .helpers.std import Std


class MangaParkMe(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/[^/]+(?:/v(\d+))?/c(\d+[^/]*)'
        idx = self.re.search(selector, self.chapter).groups()
        if idx[0] is None:
            return '0-' + idx[1]
        return '-'.join(idx)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('#list a.ch')

    def get_files(self):
        chapter = self.re.search(r'^(.+/c\d+)', self.chapter).group(1)
        content = self.http_get(chapter)
        data = self.re.search(r'var\s_load_page\s?=\s?(\[.+\])', content)
        if not data:
            return []
        json = self.json.loads(data.group(1))
        return [i['u'] for i in json]

    def get_cover(self):
        return self._cover_from_content('.cover img')


main = MangaParkMe
