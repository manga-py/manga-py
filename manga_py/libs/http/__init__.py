from pathlib import Path
from random import randint
from urllib.parse import ParseResult, urlparse
from zlib import crc32

from requests import Response
from requests.api import get, post, request

from ...exceptions import *
from ...libs import print_lib
from ...libs.log import logger
from ...libs.store import http_store, Store


class Http:
    __slots__ = ('store', 'base_url', 'logger')

    def __init__(self, base_url: str = None):
        self.store = http_store  # type: Store
        self.base_url = base_url
        self.logger = logger()

    def download(self, response: Response, destination: Path):
        self.logger.debug({
            'Method': response.request.method,
            'Url': response.request.url,
        })
        with destination.open('wb') as w:
            if not w.writable():
                raise FsError('Destination not writable. Please, check permissions')
            content = response.content
            errors = []
            if ~response.headers['Content-Type'].find('text/'):
                errors.append('Content not binary type.')
            if len(content) <= 0:
                errors.append('Response has zero length.')
                print_lib(
                    '%s Url: %s\nHistory: %s' %
                    (
                        errors[-1],
                        response.url,
                        '\n'.join(map(lambda _url: _url.url, response.history))
                    )
                )
            if len(errors) > 0:
                error_file = str(crc32(str(destination).encode()))
                with Path(error_file).open('wb') as _w:
                    _w.write(content)
                logger().warning('\n'.join(errors))
                w.close()
                destination.unlink()  # remove, if error
            else:
                w.write(content)
                w.close()
                return True

    def request(self, method, url, **kwargs):
        if self.base_url is None:
            self.base_url = url
        __doc__ = request.__doc__

        self.logger.debug({
            'Method': method,
            'Url': url,
        })

        try:
            return request(method, url, **kwargs)
        except Exception:
            raise NetworkException()

    def url_normalize(self, url):
        _url = urlparse(url)  # type: ParseResult
        if _url.scheme == '':
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

    @staticmethod
    def _domain_from_url(url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.netloc) < 1:
            raise InvalidUrlException(url)
        return fragments.netloc

    def _scheme_from_url(self, url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.scheme) < 1:
            return self.store.scheme
        return fragments.netloc

    def set_base_url(self, url):
        self.base_url = url

    def check_redirect(self, url: str) -> str:
        """
        Return new url (maybe site has redirect)
        """
        headers = self.request('head', url)
        return he

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


def check_url(url: str) -> str:
    """
    checks url for correctness
    :param url:
    :return:
    """
    check = urlparse(url)  # type: ParseResult
    if check.scheme == '':
        logger().warning('Url scheme has missing (%s). Use default scheme' % url)
        check.scheme = 'http'
    if check.netloc == '':
        logger().critical('Url netloc has missing (%s)')
        raise InvalidUrlException(url)
    return check.geturl()


__all__ = ['Http', 'default_ua']
