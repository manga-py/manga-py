from manga_py.provider import Provider
from .helpers.std import Std


class MangaGoMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        tp = self.re.search('/(mf|raw)', self.chapter).group(1)
        return 'vol_{:0>3}-{}-{}'.format(*idx, tp)

    def get_chapter_index(self) -> str:
        selector = r'/(?:mf|raw)/.*?(\d+)(?:\.(\d+))?'
        chapter = self.chapter
        idx = self.re.search(selector, chapter).groups()
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        return self._get_content('{}/read-manga/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'/read-manga/([^/]+)/')

    def get_chapters(self):
        content = self.document_fromstring(self.content, '#information', 0)
        chapters = content.cssselect('#chapter_table a.chico')
        raws = content.cssselect('#raws_table a.chicor')
        return chapters + raws

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        content = self.http_get(self.chapter)
        parser = self.re.search("imgsrcs.+[^.]+?var.+?=\s?'(.+)'", content)
        if not parser:
            return []
        return parser.group(0).split(',')

    def get_cover(self):
        return self._cover_from_content('#information .cover img')


main = MangaGoMe
