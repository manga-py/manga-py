from typing import ClassVar
from .http import *
from urllib.parse import urlparse
from .util.fs import default_headers_location


class Parser:
    _http: ClassVar[Http] = None
    _domain: ClassVar[str] = None

    def __init__(self, url: str):
        self._domain = urlparse(url).hostname
        self._http = Http(default_headers_location(
            'headers-%s.dat' % self._domain
        ))
