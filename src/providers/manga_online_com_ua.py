from src.provider import Provider


class MangaOnlineCom(Provider):
    __local_storage = None

    def __init_storage(self):
        if not self.__local_storage:
            self.__local_storage = dict()

    def get_archive_name(self) -> str:
        self.__init_storage()
        idx = self.get_chapter_index().split('-')
        return 'vol_{}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        self.__init_storage()
        idx_reg = '/\\d+.+\\-(\\d+).+?\\-(\\d+).*?html'
        idx = self.re.search(idx_reg, self.get_current_chapter()).groups()
        if not idx:
            idx_reg = '/\\d+.+\\-(\\d+).+?html'
            idx = (self.re.search(idx_reg, self.get_current_chapter()).group(1), 0)
        return '{:0>3}-{:0>3}'.format(*idx)

    def get_main_content(self):
        return ['0']

    def get_manga_name(self) -> str:
        self.__init_storage()
        if not self.__local_storage.get('chapters', False):
            self.__local_storage['chapters'] = self.get_chapters()
        if len(self.__local_storage['chapters']):
            return self.re.search('/manga/(.+)/.+\\.html', self.__local_storage['chapters'][0]).group(1)
        raise AttributeError()

    def _get_chapters_cmanga(self):
        items = self.html_fromstring(self.get_url(), '#dle-content > div > a[href*="/manga/"]')
        return [i.get('href') for i in items[::-1]]

    def _get_chapters_manga(self):
        items = self.html_fromstring(self.get_url(), '.fullstory_main select.selectmanga option')
        return [i.get('value') for i in items[::-1]]

    def get_chapters(self):
        self.__init_storage()
        if self.re.search('/cmanga/', self.get_url()):
            return self._get_chapters_cmanga()
        if self.re.search('/manga/[^/]+/\\d+\\-', self.get_url()):
            return self._get_chapters_manga()
        return []

    def prepare_cookies(self):
        pass

    def _get_pages_count(self, parser):
        _len = len(parser.cssselect('#pages_all a'))
        return _len + 1 if _len else 0

    def _get_image(self, parser):
        return parser.cssselect('img')[0].get('src')

    def get_files(self):
        chapter = self.get_current_chapter()
        parser = self.html_fromstring(chapter, '.main_body', 0)
        pages = self._get_pages_count(parser)
        images = []
        idx = self.re.search('/manga/[^/]+/(\\d+)', chapter).group(1)
        for n in range(pages):
            url = '{}/engine/ajax/sof_fullstory.php?id={}&page={}'.format(self.get_domain(), idx, n+1)
            parser = self.html_fromstring(url)[0]
            images.append(self._get_image(parser))
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaOnlineCom
