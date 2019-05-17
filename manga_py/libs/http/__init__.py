from argparse import ArgumentParser
from pathlib import Path

from requests import Response, PreparedRequest
from requests.api import get, post, request

from manga_py.libs.log import logger
from manga_py.libs.store import Store


class Http:
    __slots__ = ()
    __store = {}

    def __init__(self, args: ArgumentParser = None):
        self.__store.setdefault('store', Store)
        if args is not None:
            self.__store['args'] = args.parse_args()

    def __debug(self):
        return self.__store['args'].show_log

    def download(self, response: Response, destination: Path):
        if self.__debug():
            r = response.request  # type: PreparedRequest
            logger.debug('\n'.join([
                'Method: ' + r.method,
                'Url: ' + r.url,
            ]))
        with destination.open('wb') as w:
            if not w.writable():
                raise

    def request(self, method, url, **kwargs):
        __doc__ = request.__doc__
        if self.__debug():
            logger.debug('\n'.join([
                'Method: ' + method,
                'Url: ' + url,
            ]))
        return request(method, url, **kwargs)

    def get(self, url, params=None, **kwargs):
        __doc__ = get.__doc__
        return get(url, params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        __doc__ = post.__doc__
        return post(url, data, json, **kwargs)
