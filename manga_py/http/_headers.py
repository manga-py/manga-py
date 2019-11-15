import json
from pathlib import Path
from typing import ClassVar

from ..util import fs


class Headers:
    __headers: ClassVar[dict] = None
    __cookies: ClassVar[dict] = None

    def __init__(self, headers_file_location: Path):
        self.__headers = {}
        self.__cookies = {}
        self.load_headers(headers_file_location)

    @property
    def headers(self) -> dict:
        return self.__headers.copy()

    @headers.setter
    def headers(self, headers: dict):
        self.__headers = headers

    def update_headers(self, headers: dict):
        self.__headers.update(headers)

    @property
    def cookies(self) -> dict:
        return self.__cookies.copy()

    @cookies.setter
    def cookies(self, cookies: dict):
        self.__cookies = cookies

    def update_cookies(self, cookies: dict):
        self.__cookies.update(cookies)

    def load_headers(self, location: Path):
        location = location.resolve()
        fs.is_readable(location)
        if not location.is_file():
            return
        with open(str(location), 'r') as r:
            content = r.read()
            if len(content) < 2:
                return
            self.__headers = dict(json.loads(content))
            if 'manga-py_cookies' in self.__headers:
                self.__cookies = self.__headers['manga-py_cookies']
                del self.__headers['manga-py_cookies']

    def save_headers(self, location: Path):
        location = location.resolve()
        assert location.parent.is_dir()
        fs.is_writable(location.parent)
        with open(str(location), 'w') as w:
            headers = self.__headers.copy()
            headers['manga-py_cookies'] = self.cookies.copy()
            w.write(json.dumps(headers))

