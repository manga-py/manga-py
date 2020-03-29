from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt.base_lib import BaseLib


class MangaHereCc(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        selector = r'/manga/[^/]+/[^\d]+(\d+)/[^\d]+(\d+)'
        idx = self.re.search(selector, chapter)
        if idx:
            return '-'.join(idx.groups())
        selector = r'/manga/[^/]+/[^\d]+(\d+)'
        return self.re.search(selector, chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail-main-list a')

    def get_files(self):
        content = self.http_get(self.chapter)
        js = self.re.search(r'>eval(\(function.+\))\s*<', content).group(1)
        images = BaseLib.exec_js('var images = ' + js, 'images')
        images = self.re.findall(r'[\'"]((?:.{7,8})?//.+?)[\'"]', images)
        n = self.http().normalize_uri
        return [n(i) for i in images]

    def get_cover(self):
        return self._cover_from_content('.detail-info-cover-img')

    def prepare_cookies(self):
        self._base_cookies()
        self.http().cookies['isAdult'] = '1'


main = MangaHereCc
