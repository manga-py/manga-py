
from manga_py.provider import Provider


class Example(Provider):
    def get_content(self):
        pass

    def get_manga_name(self) -> str:
        pass

    def get_chapters(self) -> list:
        pass

    def get_files(self):
        pass

    def get_chapter_name(self):
        pass


main = Example
