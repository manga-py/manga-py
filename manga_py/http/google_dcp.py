import random
import time

from manga_py.crypt.base_lib import BaseLib
from .request import Request


class GoogleDCP:
    host = 'proxy.googlezip.net'
    authkey = 'ac4500dd3b7579186c1b0620614fdb1f7d61f944'
    http = None

    def __init__(self, http: Request):
        self.http = http

    def randint(self):
        return random.randint(0, 999999999)

    def _build_header(self):
        timestamp = int(time.time())
        md5 = BaseLib.md5('{}{}{}'.format(timestamp, self.authkey, timestamp))
        return 'Chrome-Proxy: ps={}-{}-{}-{}, sid={}, c=win, b=3029, p=110'.format(
            int(time.time()),
            self.randint(),
            self.randint(),
            self.randint(),
            BaseLib.str2hex(md5.hexdigest())
        )

    def set_proxy(self):
        self.http.proxies['http'] = self.host
        self.http.headers = self._build_header()
        return self.http
