from urllib.parse import urlparse

import requests

from .url_normalizer import UrlNormalizer


class Request:
    referrer_url = ''
    proxies = {}
    allow_webp = True
    user_agent = '%s %s %s %s' % (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/60.0.3112.101',
        'Safari/537.36'
    )
    cookies = []

    def _get_cookies(self, cookies=None):
        return cookies if cookies else self.cookies

    def _requests_helper(
            self, method, url, headers=None, cookies=None, data=None,
            files=None, max_redirects=10, timeout=None, proxies=None
    ) -> requests.Response:
        r = getattr(requests, method)(
            url=url, headers=headers, cookies=cookies, data=data,
            files=files, allow_redirects=False, proxies=proxies
        )
        if r.is_redirect:
            if max_redirects < 1:
                raise AttributeError('Too many redirects')
            location = UrlNormalizer.url_helper(r.headers['location'], self.referrer_url)
            return self._requests_helper(
                method, location, headers, cookies, data,
                files, max_redirects-1, timeout=timeout
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
        with self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='get'
        ) as response:
            text = response.text
            response.close()
            return text

    def post(self, url: str, headers: dict = None, cookies: dict = None, data: dict = (), files=None) -> str:
        with self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='post',
                data=data,
                files=files
        ) as response:
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

    def __parse_cookies(self, response: requests.Response, domain: str, cookies: dict):
            for i in cookies:
                if isinstance(i, str):
                    self.user_agent = i
                elif isinstance(i, dict):
                    response.cookies.set(
                        name=i.get('name'),
                        value=i.get('value'),
                        domain=i.get('domain', domain),
                        path=i.get('path', '/')
                    )

    def get_base_cookies(self, url: str, cookies=None):
        """
        :param url:
        :param cookies: ('User-agent', {"name": "Cookie name", "value": "Cookie value",
         "domain": "Cookie domain", "path": "Cookie path") -> tuple
        :return:
        """
        session = requests.Session()
        h = session.head(url)
        if isinstance(cookies, dict):
            _ = urlparse(self.referrer_url)
            domain = "{}://{}".format(_.scheme, _.netloc)
            self.__parse_cookies(h, domain, cookies)
        session.close()
        return h.cookies
