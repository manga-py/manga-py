from manga_py.provider import Provider
from .helpers.std import Std


class MangaReaderXyz(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chapter-(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        if ~self.get_url().find('/manga/'):
            re = '/manga/([^/]+)'
        else:
            re = '/([^/]+)/chapter-'
        return self._get_name(re)

    def get_chapters(self):
        return self._elements('.table td > a,.chapter-list div.row a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter + '/0')
        return self._images_helper(parser, '#view-chapter img,#vungdoc img')

    def get_cover(self) -> str:
        return self._cover_from_content('img.img-thumbnail,.manga-info-pic > img')

    def book_meta(self) -> dict:
        pass


main = MangaReaderXyz
