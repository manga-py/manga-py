from os import access, W_OK
from pathlib import Path

from urllib3 import PoolManager, HTTPResponse

from ._headers import Headers
from ._downloader import Downloader
from typing import ClassVar


__all__ = ['Http', 'Headers', 'Downloader']


class Http:
    _connection: ClassVar[PoolManager] = None
    _headers: ClassVar[dict] = None
    _cookies: ClassVar[dict] = None

    def __init__(self, headers_file_location: Path):
        super().__init__(headers_file_location)
        headers = Headers(headers_file_location)
        self._headers = headers.headers
        self._cookies = headers.cookies
        self._connection = PoolManager(headers=self._headers)

    def _request(self, method: str, url, headers: dict = None) -> HTTPResponse:
        _headers = self._headers
        if headers is not None:
            _headers.update(headers)
        return self._connection.request(method, url, headers=_headers)

    def get(self, url: str, headers: dict = None) -> HTTPResponse:
        return self._request('GET', url, headers=headers)

    def head(self, url: str, headers: dict = None) -> HTTPResponse:
        return self._request('HEAD', url, headers=headers)

    def post(self, url: str, headers: dict = None) -> HTTPResponse:
        return self._request('POST', url, headers=headers)

    def save_file(self, url, location: Path, method: str = 'GET'):
        location = location.resolve()
        assert location.is_dir()
        assert access(str(location.parent), mode=W_OK)
        with open(str(location), 'wb') as w:
            w.write(self._request(method, url).data)
