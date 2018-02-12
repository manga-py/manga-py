from src.provider import Provider


class MangaIndoWebId(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        selector = r'\-chapter\-([^/]+)'
        return self.re.search(selector, self.get_current_chapter()).group(1)

    def get_main_content(self):
        params = self.get_domain(), self.get_manga_name()
        return self.http_get('{}/{}/'.format(*params))

    def get_manga_name(self) -> str:
        url = self.get_url()
        pos = url.find('-chapter-')
        if pos > 0:
            item = self.html_fromstring(self.get_url(), 'article[id^="post-"]', 0)
            item = self.re.search(r'category\-([^\s]+)', item.get('class')).group(1)
            return item
        return self.re.search(r'\.id/([^/]+)', url).group(1)

    def get_chapters(self):
        selector = '.lcp_catlist li > a'
        items = self.document_fromstring(self.get_storage_content(), selector)
        return [i.get('href') for i in items]

    def get_files(self):
        r = self.http().get_redirect_url
        params = self.get_current_chapter(), '.entry-content img.aligncenter'
        items = self.html_fromstring(*params)
        return [r(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._get_cover_from_content('#m-cover > img')


main = MangaIndoWebId
