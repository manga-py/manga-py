from src.providers.authrone_com import AuthroneCom
from .helpers.std import Std


class MngCowCo(AuthroneCom, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('.')
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}'
        return fmt.format(*idx)

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.co/[^/]+/([^/]+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.co/([^/]+)')


main = MngCowCo
