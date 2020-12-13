from .authrone_com import AuthroneCom
from .helpers.std import Std


class MngCowCo(AuthroneCom, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(
            r'\.\w{2,7}/[^/]+/([^/]+)',
            self.chapter
        ).group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')


main = MngCowCo
