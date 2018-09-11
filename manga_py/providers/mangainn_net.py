from manga_py.provider import Provider
from .helpers.std import Std


class MangaInnNet(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search(r'\.net/[^/]+/([^/]+)', chapter).group(1).split('.')
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        name = self.re.search(r'\.net/([^/]+)', self.get_url())
        return name.group(1)

    def get_chapters(self):
        return self.document_fromstring(self.content, '#chapter_list a[href]')

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'var\s+images\s*=\s*(\[\{.+?\}\])', content).group(1)
        images = self.json.loads(images)
        return [i.get('url') for i in images]

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaInnNet
