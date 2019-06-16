from requests import Response, PreparedRequest
from requests.api import get, post, request

from manga_py.libs.log import logger
from manga_py.libs.store import http_store, Store
from manga_py import exceptions
from urllib.parse import ParseResult, urlparse
from pathlib import Path
from zlib import crc32
from random import randint


class Http:
    __slots__ = ('store', 'base_url')

    def __init__(self, base_url: str = None):
        self.store = http_store  # type: Store
        self.base_url = base_url

    def __debug(self):
        return self.store.arguments.show_log

    def download(self, response: Response, destination: Path):
        if self.__debug():
            r = response.request  # type: PreparedRequest
            logger().debug('\n'.join([
                '\nDownload file',
                'Method: ' + r.method,
                'Url: ' + r.url,
                ''
            ]))
        with destination.open('wb') as w:
            if not w.writable():
                raise exceptions.FsError('Destination not writable. Please, check permissions')
            content = response.content
            if not isinstance(content, bytes):
                error_file = str(crc32(str(destination).encode()))
                with Path(error_file).open('w') as _w:
                    _w.write(content)
                raise exceptions.NetworkException('Content not bytes. Check ' + error_file)
            w.write(content)

    def request(self, method, url, **kwargs):
        if self.base_url is None:
            self.base_url = url
        __doc__ = request.__doc__
        if self.__debug():
            logger().debug('\n'.join([
                'Method: ' + method,
                'Url: ' + url,
            ]))
        try:
            return request(method, url, **kwargs)
        finally:
            raise exceptions.NetworkException()

    def url_normalize(self, url):
        _url = urlparse(url)  # type: ParseResult
        if not _url.scheme:
            _url.scheme = self.store.scheme
        return _url

    @staticmethod
    def get(url, params=None, **kwargs):
        __doc__ = get.__doc__
        return get(url, params, **kwargs)

    @staticmethod
    def post(url, data=None, json=None, **kwargs):
        __doc__ = post.__doc__
        return post(url, data, json, **kwargs)

    def _domain_from_url(self, url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.netloc) < 1:
            raise exceptions.InvalidUrlException(url)
        return fragments.netloc

    def _scheme_from_url(self, url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.scheme) < 1:
            return self.store.scheme
        return fragments.netloc

    def set_base_url(self, url):
        self.base_url = url


def default_ua():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        # 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    ]
    return agents[randint(0, len(agents) - 1)]


__all__ = ['Http', 'default_ua']
