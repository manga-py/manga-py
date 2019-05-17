from typing import Optional

from ._http import HttpStore


class Store(object):
    __slots__ = ()
    _store = {}

    @property
    def content(self) -> Optional[str]:
        return self._store.get('content', None)

    @content.setter
    def content(self, val):
        self._store['content'] = val

    @property
    def name(self) -> Optional[str]:
        return self._store.get('manga-name', None)

    @name.setter
    def name(self, val):
        self._store['manga-name'] = val

    @property
    def ua(self) -> Optional[str]:
        return self._store['user-agent', None]

    @ua.setter
    def ua(self, val):
        self._store['user-agent'] = val

    @property
    def http(self) -> HttpStore:
        http = self._store.get('http', None)

        if http is None:
            http = HttpStore()
            self._store['http'] = http

        return http
