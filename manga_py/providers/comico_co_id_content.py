from .comico_co_id_titles import ComicoCoIdTitles
from .helpers.std import Std


class ComicoCoIdContent(ComicoCoIdTitles, Std):  # todo
    __origin_url = None

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return 'Fake'

    def prepare_cookies(self):
        self.__origin_url = self.get_url()

    def get_chapters(self):
        # return self._elements('a.chapter')
        return []

    def get_files(self):
        return []

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass


main = ComicoCoIdContent
