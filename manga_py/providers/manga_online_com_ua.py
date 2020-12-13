from manga_py.provider import Provider
from .helpers.std import Std


class MangaOnlineCom(Provider, Std):
    __local_storage = None

    def __init_storage(self):
        if not self.__local_storage:
            self.__local_storage = {}

    def get_chapter_index(self) -> str:
        self.__init_storage()
        idx_reg = r'/\d+.+-(\d+).+?-(\d+).*?html'
        idx = self.re.search(idx_reg, self.chapter).groups()
        if not idx:
            idx_reg = r'/\d+.+-(\d+).+?html'
            idx = (self.re.search(idx_reg, self.chapter).group(1), 0)
        return '{:0>3}-{:0>3}'.format(*idx)

    def get_content(self):
        return ['0']

    def get_manga_name(self) -> str:
        self.__init_storage()
        if not self.__local_storage.get('chapters', False):
            self.__local_storage['chapters'] = self.get_chapters()
        if len(self.__local_storage['chapters']):
            return self.re.search(r'/manga/(.+)/.+\.html', self.__local_storage['chapters'][0]).group(1)
        raise AttributeError()

    def _get_chapters_cmanga(self):
        s = '#dle-content > div > a[href*="/manga/"]'
        return self.html_fromstring(self.get_url(), s)[::-1]

    def _get_chapters_manga(self):
        s = '.fullstory_main select.selectmanga option'
        items = self.html_fromstring(self.get_url(), s)
        return [i.get('value') for i in items[::-1]]

    def get_chapters(self):
        self.__init_storage()
        if self.re.search('/cmanga/', self.get_url()):
            return self._get_chapters_cmanga()
        if self.re.search(r'/manga/[^/]+/\d+-', self.get_url()):
            return self._get_chapters_manga()
        return []

    @staticmethod
    def _get_pages_count(parser):
        _len = len(parser.cssselect('#pages_all a'))
        return _len + 1 if _len else 0

    def get_files(self):
        chapter = self.chapter
        parser = self.html_fromstring(chapter, '.main_body', 0)
        pages = self._get_pages_count(parser)
        images = []
        idx = self.re.search(r'/manga/[^/]+/(\d+)', chapter).group(1)
        for n in range(pages):
            url = '{}/engine/ajax/sof_fullstory.php?id={}&page={}'.format(self.domain, idx, n + 1)
            parser = self.html_fromstring(url)[0]
            images += self._images_helper(parser, 'img')
        return images

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaOnlineCom
