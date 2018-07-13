from abc import abstractmethod


class Abstract:
    @abstractmethod
    def get_content(self):  # return mixed
        pass

    @abstractmethod
    def get_manga_name(self) -> str:
        pass

    @abstractmethod
    def get_chapters(self) -> list:
        pass

    @abstractmethod
    def get_files(self):
        pass

    @abstractmethod
    def get_chapter_name(self):
        pass

    def get_chapter_url(self) -> str:
        pass

    def get_cover(self):
        pass

    def prepare_cookies(self):
        pass

    def book_meta(self):  # Todo
        pass
