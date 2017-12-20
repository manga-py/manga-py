from .extractor import Extractor


class _Template(Extractor):

    def get_main_content(self):  # call once
        pass

    def get_manga_name(self):  # call once
        pass

    def get_volumes(self):  # call once
        pass

    def get_cookies(self):  # if site with cookie protect
        pass

    def get_files(self):  # call ever volume loop
        pass

    def _loop_callback_volumes(self):
        pass

    def _loop_callback_files(self):
        pass


def provider():
    return _Template
