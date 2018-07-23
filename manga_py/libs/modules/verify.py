try:
    from manga_py.exceptions import InvalidUrlException
except ImportError:
    pass


def check_url(args):
    from urllib.parse import urlsplit
    url = urlsplit(args['url'])
    assert url.scheme != '', InvalidUrlException('scheme is empty')
    assert url.netloc != '', InvalidUrlException('netloc is empty')
