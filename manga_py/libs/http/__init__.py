from requests import Response, PreparedRequest
from requests.api import get, post, request

from manga_py.libs.log import logger
from manga_py.libs.store import http_store, Store
from manga_py import exceptions
from urllib.parse import ParseResult, urlparse
from pathlib import Path
from zlib import crc32


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
