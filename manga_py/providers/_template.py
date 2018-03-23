from manga_py.provider import Provider
from .helpers.std import Std


class _Template(Provider, Std):

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return ''

    def get_chapters(self):
        # return self._elements('a.chapter')
        return []

    def get_files(self):
        return []

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass


main = _Template
