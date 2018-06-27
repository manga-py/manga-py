from random import randint

import requests
from requests import Response


class Request:
    _req = None
    _headers = None
    _cookies = None
    _allow_default_redirect = False
    _max_redirects = 10

    def __init__(self):
        self._req = requests
        self._headers = {}
        self._cookies = {}

    def set_user_agent(self, agent=None):
        self._headers['User-Agent'] = self._user_agent(agent)

    def set_lang(self, lang='en-US'):
        self._headers['Accept-Language'] = '%s;q=0.9,ja-JP;q=0.8' % lang

    def set_referer(self, referer):
        self._headers['referer'] = referer

    def check_url(self, url):
        return self.request('head', url).ok

    def get(self, url, *args, **kwargs) -> Response:
        return self.request('get', url, *args, **kwargs)

    def post(self, url, *args, **kwargs) -> Response:
        kwargs['allow_redirects'] = False
        if self._allow_default_redirect:
            return self.request('post', url, *args, **kwargs)
        return self._request('post', url, *args, **kwargs)

    def request(self, method, url, *args, **kwargs) -> Response:
        request = getattr(requests, method)
        kwargs.setdefault('headers', self._headers)
        kwargs.setdefault('cookies', self._cookies)
        return request(url, *args, **kwargs)

    @staticmethod
    def _user_agent(agent=None) -> str:
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
        ]
        if agent is None:
            agent = agents[randint(0, len(agents) - 1)]
        return agent

    def _request(self, method, url, *args, **kwargs) -> Response:
        response = self.request(method, url, *args, **kwargs)
        response.raise_for_status()
        if response.is_redirect():
            if response.status_code == 303:
                return self._request('get', url, *args, **kwargs)
            if response.status_code == 305:
                location = url
                kwargs['proxy'] = {
                    'http': response.headers['location'],
                    'https': response.headers['location'],
                }
            else:
                location = response.headers['location']
            return self._request(method, location, *args, **kwargs)
        return response
