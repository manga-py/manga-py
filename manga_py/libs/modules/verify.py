try:
    from manga_py.exceptions import InvalidUrlException
except ImportError:
    from builtins import AttributeError as InvalidUrlException


def check_url(args):
    from urllib.parse import urlsplit
    url = urlsplit(args['url'])
    if url.scheme == '':
        InvalidUrlException('scheme is empty')
    if url.netloc == '':
        InvalidUrlException('netloc is empty')
