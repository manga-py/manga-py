
from manga_py.provider import Provider


# see manga_py/libs/base/abstract.py for more data
class Example(Provider):
    def get_content(self):
        self.url
        pass

    def get_manga_name(self) -> str:
        pass

    def get_chapters(self) -> list:
        pass

    def get_files(self) -> list:
        pass

    def get_chapter_name(self) -> tuple:
        pass

    def get_chapter_url(self) -> str:
        pass

    def get_cover(self):
        pass

    def prepare_cookies(self):
        pass

    def book_meta(self):
        pass


main = Example
