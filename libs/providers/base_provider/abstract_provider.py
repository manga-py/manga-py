from abc import abstractmethod


class AbstractProvider:

    @abstractmethod
    def get_main_content(self):  # call once
        pass

    @abstractmethod
    def get_manga_name(self) -> str:  # call once
        return ''

    @abstractmethod
    def get_chapters(self) -> list:  # call once
        return []

    @abstractmethod
    def get_cookies(self):  # if site with cookie protect
        pass

    @abstractmethod
    def get_files(self) -> list:  # call ever volume loop
        return []

    @abstractmethod
    def _loop_callback_volumes(self):
        pass

    @abstractmethod
    def _loop_callback_files(self):
        pass

    @abstractmethod
    def get_archive_name(self):
        pass
