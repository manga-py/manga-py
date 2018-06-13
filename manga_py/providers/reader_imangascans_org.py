from manga_py.provider import Provider
from .helpers.std import Std


class ReaderIMangaScansOrg(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.search(r'://.+?/[^/]+/([^/]+)', self.chapter)
        return re.group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'://.+?/([^/]+)')

    def get_chapters(self):
        sel = '.subnav-bind-top > .controls > div > .dropdown-menu li a'
        return self._elements(sel)

    def get_files(self):
        try:
            content = self.http_get(self.chapter)
            items = self.re.search(r'var\s+pages\s*=\s*(\[.+\])', content)
            items = self.json.loads(items.group(1))
            url = items[0]
            del items[0]
            return ['{}/{}{}'.format(self.domain, url, i) for i in items]
        except Exception:
            return []

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReaderIMangaScansOrg
