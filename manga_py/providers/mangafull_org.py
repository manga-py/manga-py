from manga_py.provider import Provider
from .helpers.std import Std


class MangaFullOrg(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile('\w/chapter-(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.content .chapter-list a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter + '/0')
        return self._images_helper(parser, '.each-page > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.cover-detail > img')


main = MangaFullOrg
