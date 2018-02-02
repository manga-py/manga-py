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

    def prepare_cookies(self):
        pass

    def get_files(self):
        return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = _Template
