from urllib.parse import urlparse

import requests

from .url_normalizer import UrlNormalizer


class Request:
    __redirect_base_url = ''
    referrer_url = ''
    proxies = None
    allow_webp = True
    user_agent = '%s %s %s %s' % (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/60.0.3112.101',
        'Safari/537.36'
    )
    cookies = None

    def __init__(self):
        self.proxies = {}
        self.cookies = {}

    def _get_cookies(self, cookies=None):
        return cookies if cookies else self.cookies

    def _prepare_redirect_base_url(self, url):
        if not self.__redirect_base_url:
            self.__redirect_base_url = url

    def _requests_helper(
            self, method, url, headers=None, cookies=None, data=None,
            files=None, max_redirects=10, timeout=None, proxies=None
    ) -> requests.Response:
        self._prepare_redirect_base_url(url)
        r = getattr(requests, method)(
            url=url, headers=headers, cookies=cookies, data=data,
            files=files, allow_redirects=False, proxies=proxies
        )
        if r.is_redirect:
            if max_redirects < 1:
                raise AttributeError('Too many redirects')
            location = UrlNormalizer.url_helper(r.headers['location'], self.__redirect_base_url)
            return self._requests_helper(
                method=method, url=location, headers=headers,
                cookies=cookies, data=data, files=files,
                max_redirects=(max_redirects-1),
                timeout=timeout, proxies=proxies
            )
        return r

    def _requests(
            self, url: str, headers: dict=None, cookies: dict=None,
            data=None, method='get', files=None, timeout=None
    ) -> requests.Response:
        if not headers:
            headers = {}
        cookies = self._get_cookies(cookies)
        headers.setdefault('User-Agent', self.user_agent)
        headers.setdefault('Referer', self.referrer_url)
        if self.allow_webp:
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=1.0,image/webp,image/apng,*/*;q=1.0'
        return self._requests_helper(
            method=method, url=url, headers=headers, cookies=cookies,
            data=data, files=files, timeout=timeout, proxies=self.proxies
        )

    def get(self, url: str, headers: dict = None, cookies: dict = None) -> str:
        response = self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='get'
        )
        text = response.text
        response.close()
        return text

    def post(self, url: str, headers: dict = None, cookies: dict = None, data: dict = (), files=None) -> str:
        response = self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='post',
                data=data,
                files=files
        )
        text = response.text
        response.close()
        return text

    def reset_proxy(self):
        self.proxies = {}

    def set_proxy(self, proxy):
        self.reset_proxy()
        if isinstance(proxy, dict):
            self.proxies['http'] = proxy.get('http', None)
            self.proxies['https'] = proxy.get('https', None)
        elif isinstance(proxy, str):
            self.proxies['http'] = proxy

    def get_base_cookies(self, url: str):
        """
        :param url:
        :return:
        """
        session = requests.Session()
        h = session.head(url)
        session.close()
        return h.cookies
