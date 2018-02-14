from src.provider import Provider
from .helpers.std import Std


class MangaShiroNet(Provider, Std):
    alter_re_name = r'\.net/([^/]+)\-\d+'
    chapter_re = r'\.net/[^/]+\-(\d+(?:\-\d+)?)'
    chapters_selector = 'span.leftoff > a'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        return self.re.search(self.chapter_re, chapter).group(1)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}/'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        url = self.get_url()
        if url.find('/manga/') > 0:
            re = '/manga/([^/]+)'
        else:
            re = self.alter_re_name
        return self.re.search(re, url).group(1)

    def get_chapters(self):
        return self._chapters(self.chapters_selector)

    def get_files(self):
        url = self.get_current_chapter()
        parser = self.html_fromstring(url)
        items = parser.cssselect('#readerarea a[imageanchor]')
        attr = 'href'
        if not items:
            items = parser.cssselect('#readerarea img[id]')
            attr = 'src'
        return [i.get(attr) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('img.attachment-post-thumbnail')


main = MangaShiroNet
