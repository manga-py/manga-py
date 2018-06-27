import json
from manga_py.libs.fs import storage


class Http:
    _cookies_file = storage('cookies.json')
    _cookies = None
    _headers = None
    _domain = None

    def __init__(self):
        self._headers = {}
        self._cookies = self._load_storage_cookies()

    def cookies(self):
        if self._domain is None:
            raise AttributeError('Domain is undefined')
        return self._cookies.get(self._domain)

    def _load_storage_cookies(self, domain: str = None) -> dict:
        cookies = {}
        if self._cookies_file:
            with open(self._cookies_file, 'r') as f:
                cookies = json.loads(f.read())
        return cookies.get(domain, {})

    def _dump_storage_cookies(self, cookies: dict, domain: str = None):
        if domain is not None:
            all_cookies = self._load_storage_cookies()
            all_cookies.update({domain: cookies})
        else:
            all_cookies = cookies
        with open(self._cookies_file, 'w') as f:
            f.write(json.dumps(all_cookies))

    def get(self, url, **kwargs):
        pass

    def request(self, method, url, **kwargs):
        pass

    def set_referer(self, referer):
        self._headers['referer'] = referer
