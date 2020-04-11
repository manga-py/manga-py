from manga_py.provider import Provider
from .helpers.std import Std


class Manhwa18Net(Provider, Std):

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        pass

    def get_chapters(self) -> list:
        pass

    def get_files(self) -> list:
        pass

    def get_chapter_index(self) -> str:
        pass


main = Manhwa18Net
