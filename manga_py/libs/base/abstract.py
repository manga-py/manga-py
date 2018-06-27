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

    def chapter_url(self) -> str:
        pass

    def cover(self):
        pass

    def prepare_cookies(self):
        pass

    def book_meta(self):  # Todo
        pass

    def before_chapter(self):
        pass

    def after_chapter(self):
        pass

    def before_file_save(self, url: str, idx: int) -> str:  # return url!
        return url

    def after_file_save(self, _path, idx: int):
        pass
