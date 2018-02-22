from src.provider import Provider
from .helpers.std import Std


class ReadEgScansCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        if len(idx) > 1:
            f = 'vol_{:0>3}-{}'
        else:
            f = 'vol_{:0>3}'
        return f.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/Chapter_(\d+)(.*)', self.get_current_chapter())
        return self._join_groups(idx.groups())

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content())
        items = self._first_select_options(parser, 'select[name="chapter"]', False)
        url = '%s/%s/{}' % (self.get_domain(), self.get_manga_name())
        return [url.format(i.get('value')) for i in items[::-1]]

    def get_files(self):
        url = self.get_current_chapter()
        content = self.http_get(url)
        items = self.re.findall(r'img_url\.push\s?\(\s?\'(.+)\'\s?\)', content)
        domain = self.get_domain()
        return ['{}/{}'.format(domain, i) for i in items]

    def get_cover(self) -> str:
        pass


main = ReadEgScansCom
