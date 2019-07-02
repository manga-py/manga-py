from requests import Response
from requests.cookies import RequestsCookieJar
from requests.models import cookiejar_from_dict
from urllib import parse
from typing import Union, Optional


class HttpStore(object):  # todo
    __slots__ = ('_store',)

    def __init__(self):
        self._store = {}

    @staticmethod
    def _response2url(resp: Response):
        url = resp.url
        if len(url.history):
            url = str(resp.history[-1].url)
        return url

    @staticmethod
    def _domain(url: Union[Response, str]) -> str:
        if isinstance(url, Response):
            url = HttpStore._response2url(url)
        r = parse.urlsplit(url)
        return r[1]  # netloc

    @staticmethod
    def normalize(base: Union[Response, str], url: str):
        if isinstance(url, Response):
            url = HttpStore._response2url(url)
        return parse.urljoin(base, url)

    def init(self, url: str, cookies: dict = None):
        if cookies is None:
            cookies = {}
        domain = self._domain(url)
        self._store['cookies'][domain] = cookiejar_from_dict(cookies)

    def get_cookies(self, url) -> Optional[RequestsCookieJar]:
        domain = self._domain(url)
        return self._store.get('cookies', {}).get(domain, None)

    def set_cookies(self, url, response: Response):
        cookies = response.cookies  # type: RequestsCookieJar
        domain = self._domain(url)
        self._store['cookies'][domain] = cookies

    def cookies_auto_update(self, response: Response):
        for i in response.history[::-1]:  # type: Response
            domain = self._domain(i.url)
            self._store['cookies'][domain].update(i)
        domain = self._domain(response.url)
        self._store['cookies'][domain].update(response)
