from manga_py.exceptions import InvalidUrlException


class Verify:
    _args = None

    def __init__(self, args: dict):
        self._args = args

    def check(self):
        self.url()

    def url(self):
        from urllib.parse import urlsplit
        url = urlsplit(self._args['url'])
        assert url.scheme != '', InvalidUrlException('scheme is empty')
        assert url.netloc != '', InvalidUrlException('netloc is empty')
