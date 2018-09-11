from manga_py.provider import Provider
from .helpers.std import Std


class MangaClubRu(Provider, Std):
    local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return self.normal_arc_name({'vol': idx[0], 'ch': idx[1]})

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/manga/view/[^/]+/v(\d+)-c(\d+).html')
        return '{}-{}'.format(*idx.groups())

    def get_main_content(self):
        if not self.local_storage:
            self.get_manga_name()
        return self.http_get('{}/{}.html'.format(self.domain, self.local_storage[0]))

    def get_manga_name(self) -> str:
        selector = r'\.ru(?:/manga/view)?/(?:(\d+-.+)/(.+)\.html)'
        html = self.re.search(selector, self.get_url())
        self.local_storage = html.groups()
        return self.local_storage[1]

    def get_chapters(self):
        selector = '.manga-ch-list-item > a[href^="http"]'
        return self.document_fromstring(self.content, selector)

    def get_files(self):
        result = self.html_fromstring(self.chapter, '.manga-lines-page a.manga-lines')
        return [i.get('data-i') for i in result]

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaClubRu
