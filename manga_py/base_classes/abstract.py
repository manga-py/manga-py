import time
from abc import abstractmethod
from logging import info


class Abstract:

    @abstractmethod
    def get_content(self):  # call once
        pass

    @abstractmethod
    def get_manga_name(self) -> str:  # call once
        return ''

    @abstractmethod
    def get_chapters(self) -> list:  # call once
        return []

    def prepare_cookies(self):  # if site with cookie protect
        pass

    @abstractmethod
    def get_files(self) -> list:  # call ever volume loop
        return []

    # @abstractmethod
    # def get_archive_name(self) -> str:
    #     pass

    #  for chapters selected by manual (cli)
    @abstractmethod
    def get_chapter_index(self) -> str:
        pass

    def book_meta(self) -> dict:
        pass

    def before_download_chapter(self):
        pass

    def after_download_chapter(self):
        pass

    def get_cover(self):
        pass

    def before_file_save(self, url, idx) -> str:  # return url !
        return url

    def after_file_save(self, _path: str, idx: int):
        self._wait_after_file()
        return _path, None

    @abstractmethod
    def chapter_for_json(self) -> str:
        pass

    def _wait_after_file(self):
        if hasattr(self, '_params'):
            wait_time = self._params.get('wait_after_page', 0)

            if wait_time > 0:
                info(f'Wait {wait_time} second(s) / file')
                time.sleep(wait_time)

    def _wait_after_chapter(self):
        if hasattr(self, '_params'):
            wait_time = self._params.get('wait_after_chapter', 0)

            if wait_time > 0:
                info(f'Wait {wait_time} second(s) / chapter')
                time.sleep(wait_time)
