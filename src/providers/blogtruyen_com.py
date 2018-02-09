from src.provider import Provider


class BlogTruyenCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('\\.com/c(\\d+)/', self.get_current_chapter())
        return '{}-{}'.format(self._chapter_index(), idx.group(1))

    def get_main_content(self):
        url = self._test_main_url(self.get_url())
        return self.http_get(self.http().normalize_uri(url))

    def _test_main_url(self, url):
        if url.find('.com/c') > 0:
            selector = '.breadcrumbs a + a'
            url = self.html_fromstring(url, selector, 0).get('href')
        return url

    def get_manga_name(self) -> str:
        url = self._test_main_url(self.get_url())
        return self.re.search('/\\d+/([^/]+)', url).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), '#list-chapters .title > a'
        return self.document_fromstring(c, s)

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '#content img')
        return [i.get('src') for i in items]

    def get_cover(self) -> str:
        return self._get_cover_from_content('.thumbnail img')


main = BlogTruyenCom
