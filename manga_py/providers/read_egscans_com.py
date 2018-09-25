from manga_py.provider import Provider
from .helpers.std import Std


class ReadEgScansCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/Chapter_(\d+)(.*)', self.chapter)
        return self._join_groups(idx.groups())

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        items = self._first_select_options(parser, 'select[name="chapter"]', False)
        url = '%s/%s/{}' % (self.domain, self.manga_name)
        return [url.format(i.get('value')) for i in items[::-1]]

    def get_files(self):
        url = self.chapter
        content = self.http_get(url)
        items = self.re.findall(r'img_url\.push\s?\(\s?\'(.+)\'\s?\)', content)
        domain = self.domain
        return ['{}/{}'.format(domain, i) for i in items]

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadEgScansCom
