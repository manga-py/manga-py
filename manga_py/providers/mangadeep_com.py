from .helpers.std import Std
from .mangaonline_today import MangaOnlineToday


class MangaDeepCom(MangaOnlineToday, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.\w{2,7}/[^/]+/([^/]+)', self.chapter)
        return idx.group(1)

    def document_fromstring(self, body, selector: str = None, idx: int = None):
        if ~body.find('<?'):
            body = self.re.sub(r'<\?', '', body)
        return super().document_fromstring(body, selector, idx)

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        selector = 'ul.lst a.lst'
        items = self.document_fromstring(self.content, selector)
        pages = self.document_fromstring(self.content, '.pgg li > a')
        if pages:
            idx = self.re.search(r'-list/(\d+)', pages[-1].get('href'))
            for i in range(1, int(idx.group(1))):
                content = self.http_get('{}/{}/chapter-list/{}/'.format(
                    self.domain,
                    self.manga_name,
                    i + 1
                ))
                items += self.document_fromstring(content, selector)
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('img.cvr')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaDeepCom
