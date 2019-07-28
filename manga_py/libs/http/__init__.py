from pathlib import Path
from random import randint
from typing import Tuple
from urllib.parse import ParseResult, urlparse, urljoin
from zlib import crc32

from requests import Response
from requests.api import request

from manga_py import cli
from manga_py.exceptions import *
from manga_py.libs.log import logger
from manga_py.libs.store import http_store, store


class Http:
    __slots__ = ('http_store', 'store', 'base_url', 'logger', 'provider')

    def __init__(self, provider=None, base_url: str = None):
        from manga_py.libs.provider import Provider
        if not isinstance(provider, Provider):
            raise AttributeError('provider is not Provider type')
        self.provider = provider  # type: Provider
        self.http_store = http_store  # type: http_store
        self.store = store  # type: store
        self.base_url = base_url
        self.logger = logger()
        self.http_store.init(base_url)

    def download(self, response: Response, destination: Path) -> bool:
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
                cli.syslog(
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
                logger().warning('Non-byte response. See {}'.format(error_file))
                logger().warning('\n'.join(errors))
                w.close()
                destination.unlink()  # remove, if error
            else:
                w.write(content)
                w.close()
                return True
        return False

    def request(self, method, url, **kwargs) -> Response:
        if self.base_url is None:
            self.base_url = url

        headers = kwargs.get('headers', {})
        headers.setdefault('User-Agent', self.store.ua)
        headers.setdefault('referer', self.provider.content_referer())
        kwargs.setdefault('headers', headers)
        kwargs.setdefault('cookies', self.http_store.get_cookies(url))
        # content_referer

        self.logger.debug({
            'User-Agent': self.store.ua,
            'Method': method,
            'Url': url,
        })

        try:
            req = request(method, url, **kwargs)
            self.http_store.cookies_auto_update(req)
            return req
        except Exception:
            raise NetworkException()

    @staticmethod
    def url_normalize(self, url) -> str:
        _url = urlparse(url)  # type: ParseResult
        if _url.scheme == '':
            _url.scheme = self.store.scheme
        return str(urljoin(self.base_url, _url))

    def get(self, url, params=None, **kwargs) -> Response:
        kwargs['method'] = 'get'
        kwargs['params'] = params
        kwargs['url'] = url
        return self.request(**kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        kwargs['method'] = 'post'
        kwargs['data'] = data
        kwargs['json'] = json
        kwargs['url'] = url
        return self.request(**kwargs)

    @staticmethod
    def _domain_from_url(url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.netloc) < 1:
            raise InvalidUrlException(url)
        return fragments.netloc

    def _scheme_from_url(self, url):
        fragments = urlparse(url)  # type: ParseResult
        if len(fragments.scheme) < 1:
            return self.http_store.scheme
        return fragments.netloc

    def set_base_url(self, url):
        self.base_url = url

    def check_redirect(self, url: str) -> Tuple[bool, str]:
        """
        Return new url (maybe site has redirect)
        :return (is_redirect: bool, actual_url: str)
        """
        response = self.request('head', url)
        history = response.history
        return len(history) > 0, response.url


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


__all__ = ['Http', 'default_ua', 'check_url']
