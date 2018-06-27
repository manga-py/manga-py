import json

from manga_py.libs.fs import make_dirs, is_file, dirname
from manga_py.libs.fs import storage
from .normalize import normalize
from .request import Request


class Http(Request):
    _cookies_file = storage('cookies.json')
    _domain = None
    _base_uri = None
    _accept = '*/*;q=0.9,text/html,application/xhtml+xml,application/xml;q=0.8,text/css;q=0.1'

    def __init__(self, base_uri: str = None):
        super().__init__()
        self._headers = {}
        self._cookies = self._load_storage_cookies()
        self._base_uri = base_uri

    def cookies(self):
        if self._domain is None:
            raise AttributeError('Domain is undefined')
        return self._cookies.get(self._domain)

    def set_headers(self, headers: dict):
        headers.setdefault('Accept', self._accept)
        headers.setdefault('User-Agent', self._user_agent())
        headers.setdefault('Accept-Encoding', 'gzip, deflate')

    def allow_webp(self):
        self._headers['Accept'] = 'image/webp,image/apng,' + self._accept

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

    def _normalize_uri(self, uri):
        if self._base_uri is not None:
            return normalize(uri, self._base_uri)
        return uri

    def download(self, url, path_location, method='get'):
        if is_file(path_location):
            raise FileExistsError('File %s exists!' % path_location)
        make_dirs(dirname(path_location))
        with open(path_location, 'wb') as w:
            w.write(self.request(method, url).content)
