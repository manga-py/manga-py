from src.provider import Provider


class _Template(Provider):

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return ''

    def get_chapters(self):
        return []

    def get_files(self):
        return []

    def get_cover(self) -> str:
        return self._get_cover_from_content('#gd1 > div')


main = _Template
