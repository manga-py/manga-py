from manga_py.provider import Provider
from .helpers.std import Std


class MangaHasuSe(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile('chapter-+(\d+)(?:-+(\d+))?')
        idx = re.search(self.chapter).groups()
        if idx[1] is not None:
            return '{}-{}'.format(*idx)
        return idx[0]

    def get_main_content(self):
        url = self.get_url()
        test = self.re.search(r'\.\w{2,5}/[^/]+-p\d+.html', url)
        if not test:
            self.cf_protect(self.get_url())
            url = self.html_fromstring(url, 'a.itemcrumb.active', 0).get('href')
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,5}/([^/]+)(?:-p\d+.html|/)')

    def get_chapters(self):
        return self._elements('.list-chapter .name a')

    def get_files(self):
        if not self._params.get('cf-protect'):
            self.cf_protect(self.chapter)
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.img > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.info-img > img')

    def book_meta(self) -> dict:
        pass


main = MangaHasuSe
