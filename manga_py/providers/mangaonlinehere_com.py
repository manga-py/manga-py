from manga_py.provider import Provider
from .helpers.std import Std


class MangaOnlineHereCom(Provider, Std):
    __local_storage = None

    def get_chapter_index(self) -> str:
        selector = r'/read-online/[^/]+?(\d+)(?:.(\d+))?'
        idx = self.re.search(selector, self.chapter)
        return '-'.join([
            idx[0],
            0 if idx[1] is None else idx[1]
        ])

    def get_main_content(self):
        return self._get_content('{}/manga-info/{}')

    def get_manga_name(self) -> str:
        if not self.__local_storage.get('name', None):
            url = self.get_url()
            if self.re.search(r'/read-online/', url):
                url = self.html_fromstring(url, '.back-info a', 0).get('href')
            name = self.re.search('/manga-info/Fuuka', url).group(1)
            self.__local_storage['name'] = name
        return self.__local_storage['name']

    def get_chapters(self):
        return self._elements('.list-chapter a')

    def prepare_cookies(self):
        self.__local_storage = {}

    def get_files(self):
        items = self.html_fromstring(self.chapter, '#list-img img')
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('.image-info img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaOnlineHereCom
