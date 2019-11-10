from os import access, W_OK
from pathlib import Path

from urllib3 import PoolManager, HTTPResponse

from .headers import Headers


class Http(Headers):
    connection = None

    def __init__(self, headers_file_location: Path = None):
        super().__init__(headers_file_location)
        self.connection = PoolManager(headers=self.headers)

    def _request(self, method: str, url, headers: dict = None) -> HTTPResponse:
        _headers = self.headers
        if headers is not None:
            _headers.update(headers)
        return self.connection.request(method, url, headers=_headers)

    def get(self, url: str, headers: dict = None):
        return self._request('GET', url, headers=headers)

    def head(self, url: str, headers: dict = None):
        return self._request('HEAD', url, headers=headers)

    def post(self, url: str, headers: dict = None):
        return self._request('POST', url, headers=headers)

    def save_file(self, url, location: Path, method: str = 'GET'):
        location = location.resolve()
        assert location.is_dir()
        assert access(str(location.parent), mode=W_OK)
        with open(str(location), 'wb') as w:
            w.write(self._request(method, url).data)
