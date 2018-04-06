from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt import AcQqComCrypt


class AcQqCom(Provider, Std):
    _decoder = None

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
        idx = self._get_name(r'/id/(\d+)')

    def get_manga_name(self) -> str:
        return ''

    def get_chapters(self):
        return self._elements('.chapter-page-all li a')

    def get_files(self):
        data = self._decoder.decode()
        return []

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def prepare_cookies(self):
        self._decoder = AcQqComCrypt(self)
        self._base_cookies()


main = AcQqCom
