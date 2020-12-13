from manga_py.provider import Provider
from .helpers.std import Std


class MangaIndoWebId(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'-chapter-([^/]+)'
        return self.re.search(selector, self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        url = self.get_url()
        pos = url.find('-chapter-')
        if pos > 0:
            item = self.html_fromstring(self.get_url(), 'article[id^="post-"]', 0)
            item = self.re.search(r'category-([^\s]+)', item.get('class')).group(1)
            return item
        return self.re.search(r'\.id/([^/]+)', url).group(1)

    def get_chapters(self):
        return self._elements('.lcp_catlist li > a')

    def get_files(self):
        r = self.http().get_redirect_url
        params = self.chapter, '.entry-content img.aligncenter'
        items = self.html_fromstring(*params)
        return [r(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('#m-cover > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaIndoWebId
