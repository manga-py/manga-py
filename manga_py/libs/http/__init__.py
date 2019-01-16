import json

from manga_py.libs import fs
from .request import Request
from urllib.parse import urljoin


class Http(Request):
    _cookies_file = fs.storage('cookies.json')
    _base_uri = None
    _accept = '*/*;q=0.9,text/html,application/xhtml+xml,application/xml;q=0.8,text/css;q=0.1'

    def __init__(self, base_uri: str = None):
        super().__init__()
        self._headers = {}
        self._cookies = self._load_storage_cookies()
        self._base_uri = base_uri

    def set_headers(self, headers: dict = None):
        if headers is None:
            headers = {}
        headers.setdefault('Accept', self._accept)
        headers.setdefault('User-Agent', self._user_agent())
        headers.setdefault('Accept-Encoding', 'gzip, deflate')
        super().set_headers(headers)

    def allow_webp(self, url):
        self._headers['Accept'] = 'image/webp,image/apng,' + self._accept

    def _load_storage_cookies(self, domain: str = None) -> dict:
        cookies = {}
        if fs.is_file(self._cookies_file):
            with open(self._cookies_file, 'r') as f:
                cookies = json.loads(f.read())
        if domain is None:
            return cookies
        return cookies.get(domain, {})

    def _dump_storage_cookies(self, cookies: dict, domain: str = None):
        if domain is not None:
            all_cookies = self._load_storage_cookies()
            all_cookies.update({domain: cookies})
        else:
            all_cookies = cookies
        if fs.is_file(self._cookies_file):
            with open(self._cookies_file, 'w') as f:
                f.write(json.dumps(all_cookies))

    def normalize_uri(self, uri):
        if self._base_uri is not None:
            return urljoin(self._base_uri, uri)
        return uri

    def download(self, url, path_location, method='get'):
        if fs.is_file(path_location):
            raise FileExistsError('File %s exists!' % path_location)
        fs.make_dirs(fs.dirname(path_location))
        part = path_location + '.part'
        mode = 'wb'
        headers = self._headers.copy()
        if fs.is_file(part):  # resume
            part_size = fs.file_size(part)
            if ~part_size:
                mode = 'ab'
                headers['Range'] = 'bytes=%d-' % fs.file_size(part)
        with open(part, mode) as w:
            w.write(self.request(method, url, headers=headers).content)
        fs.rename(part, path_location)

    def cookies(self, url=None):
        if url is None:
            url = self._base_uri
        return super().cookies(url)

    def headers(self):
        return self._headers
