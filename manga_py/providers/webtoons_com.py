from manga_py.provider import Provider
from .helpers.std import Std


class WebToonsCom(Provider, Std):
    __titleNo = 0
    __mainUrl = ''
    __next_page_urls = None

    def get_archive_name(self) -> str:
        i = self.re.search(r'\.com%s%s' % (
            r'(?:/|%2F)[^/%]+' * 3,
            r'(?:/|%2F)([^/%]+)',
        ), self.chapter)
        return self.normal_arc_name([self.chapter_id, i.group(1)])

    def get_chapter_index(self) -> str:
        return self.re.search(r'\bepisode_no=(\d+)', self.chapter).group(1)

    def get_main_content(self):
        return self.http_get(self.__mainUrl)

    def get_manga_name(self) -> str:
        self.__titleNo = self._get_name(r'title_no=(\d+)')
        name = self._get_name(r'\.com/([^/]+/[^/]+/[^/]+)')
        self.__mainUrl = '{}/{}/list?title_no={}'.format(self.domain, name, self.__titleNo)
        return self._get_name(r'\.com/[^/]+/[^/]+/([^/]+)')

    def _chapters(self, content):
        return self._elements('#_listUl li > a', content)

    def _get_page_urls(self, content):
        return self._elements('.paginate a:not([class]):not([onclick])', content)

    def _get_pages_urls(self, content):
        chapters = []
        n = self.http().normalize_uri
        for j in self._get_page_urls(content):  # page-urls
            _content = self.http_get(n(j.get('href')))
            chapters += self._chapters(_content)
        return chapters

    def get_next_page_urls(self, content):
        urls = self._elements('a + a.pg_next', content)
        n = self.http().normalize_uri
        if len(urls):
            self.__next_page_urls.append(n(urls[0].get('href')))
            _content = self.http().get(n(urls[0].get('href')))
            self.get_next_page_urls(_content)

    def get_chapters(self):
        print('Parse chapters. Please, wait')
        self.__next_page_urls = []
        chapters = self._chapters(self.content)
        n = self.http().normalize_uri
        chapters += self._get_pages_urls(self.content)  # main page paginator

        self.get_next_page_urls(self.content)
        for url in self.__next_page_urls:
            content = self.http().get(n(url))
            chapters += self._chapters(content)
            chapters += self._get_pages_urls(content)

        return chapters

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#_imageList img', 'data-url')

    def get_cover(self) -> str:
        img = self.html_fromstring(self.content, '#content > .detail_bg', 0)
        return self.parse_background(img)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = WebToonsCom
