from src.providers.mangaonline_today import MangaOnlineToday
from .helpers.std import Std


class MangaDeepCom(MangaOnlineToday, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.com/[^/]+/([^/]+)', self.chapter)
        return idx.group(1)

    def document_fromstring(self, body, selector: str = None, idx: int = None):
        if ~body.find('<?'):
            body = self.re.sub(r'<\?', '', body)
        return super().document_fromstring(body, selector, idx)

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self.document_fromstring(self.content, 'ul.lst a.lst')

    def get_cover(self) -> str:
        return self._cover_from_content('img.cvr')


main = MangaDeepCom
