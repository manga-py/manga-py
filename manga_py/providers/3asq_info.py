from .authrone_com import AuthroneCom
from .helpers.std import Std


class ThreeAsqInfo(AuthroneCom, Std):
    _ch_selector = '.mng_det ul.lst > li > a.lst'

    def get_chapter_index(self) -> str:
        return self.re.search(
            r'\.info/[^/]+/([^/]+)',
            self.chapter
        ).group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.info/([^/]+)')

    def get_files(self):
        return list(set(super().get_files()))  # remove doubles


main = ThreeAsqInfo
