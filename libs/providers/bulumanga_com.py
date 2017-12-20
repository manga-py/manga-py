from .extractor import Extractor


class Bulumanga(Extractor):
    domainUri = 'http://bulumanga.com'

    def get_main_content(self):
        return self.http_get(self.domainUri)

    def get_manga_name(self):
        pass

    def get_volumes(self):
        pass

    def get_cookies(self):
        pass

    def get_files(self):
        pass

    def _loop_callback_volumes(self):
        pass

    def _loop_callback_files(self):
        pass


def provider():
    return Bulumanga
