import requests
from .request import Request


class CfHttp:
    __ua = 'Mozilla/5.0'

    def __init__(self, cf_proxy: str, ua: str = Request.user_agent):
        self.cf_proxy = cf_proxy
        self.__ua = ua

    def get(self, url, **kwargs) -> requests.Response:
        return self.__req('get', '')

    def __req(self, method, url, **kwargs) -> requests.Response:
        headers = kwargs.get('headers', {})
        kwargs.update({
            'cmd': f'request.{method}',
            'url': url,
            'userAgent': headers.get('User-Agent', self.__ua),
            'maxTimeout': int(kwargs.get('maxTimeout', 60000)),
        })
        return requests.post(f'{self.cf_proxy}/v1', **kwargs)
