from .provider import Provider


class ReadmangaMe(Provider):

    def get_main_content(self):
        url = '{}/{}?mature=1&mtr=1'.format(self.get_domain(), self.get_manga_name())
        return self.http_get(url)

    def get_manga_name(self):
        return self.re.search('\\.me/([^/]+)', self.get_url())

    def get_chapters(self):
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
    return ReadmangaMe
