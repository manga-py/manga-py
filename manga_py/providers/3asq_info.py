from .authrone_com import AuthroneCom
from .helpers.std import Std


class ThreeAsqInfo(AuthroneCom, Std):
    _ch_selector = '.mng_det ul.lst > li > a.lst'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('.')
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.info/[^/]+/([^/]+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.info/([^/]+)')

    def get_files(self):
        return list(set(super().get_files()))  # remove doubles


main = ThreeAsqInfo
