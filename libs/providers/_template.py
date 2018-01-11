from .provider import Provider


class _Template(Provider):

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):  # call once
        pass

    def get_manga_name(self):  # call once
        return ''

    def get_chapters(self):  # call once
        return []

    def get_cookies(self):  # if site with cookie protect
        pass

    def get_files(self):  # call ever volume loop
        return []

    def _loop_callback_volumes(self):
        pass

    def _loop_callback_files(self):
        pass


def provider():
    return _Template
