from manga_py.provider import Provider
from .helpers.std import Std


class MangaShiroNet(Provider, Std):
    _main_prefix = None

    alter_re_name = r'\.\w{2,7}/([^/]+)-\d+'
    chapter_re = r'\.\w{2,7}/[^/]+-(\d+(?:-\d+)?)'
    chapters_selector = 'span.leftoff > a,#chapterlist .eph-num > a'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        return self.re.search(self.chapter_re, chapter).group(1)

    def get_content(self):
        return self._get_content('{}/%s/{}/' % self._main_prefix)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/%s/' % self._main_prefix):
            re = ('/%s/([^/]+)' % self._main_prefix)
        else:
            re = self.alter_re_name
        return self.re.search(re, url).group(1)

    def get_chapters(self):
        return self._elements(self.chapters_selector)

    def get_files(self):
        url = self.chapter
        parser = self.html_fromstring(url)
        items = parser.cssselect('#readerarea a[imageanchor]')
        attr = 'href'
        if not items:
            items = parser.cssselect('#readerarea img[id]')
            attr = 'src'
        return [i.get(attr) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('img.attachment-post-thumbnail')

    def prepare_cookies(self):
        self._main_prefix = self.re.search(r'/(comics?|manga)/', self.get_url()).group(1)


main = MangaShiroNet
