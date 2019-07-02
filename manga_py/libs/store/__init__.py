from typing import Optional

from ...cli.args.args_helper import ArgsListHelper
from ...libs.store._http import HttpStore


class Store(object):
    """
    Global app store
    """
    _store = {}
    @property
    def arguments(self) -> ArgsListHelper:
        return self._store['arguments']

    @arguments.setter
    def arguments(self, arguments):
        self._store['arguments'] = arguments

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
        return self._store.get('user-agent', None)

    @ua.setter
    def ua(self, val):
        self._store['user-agent'] = val

    @property
    def scheme(self):
        return self._store.get('scheme', 'https')

    @scheme.setter
    def scheme(self, scheme: str):
        if scheme not in ['http', 'https']:
            raise RuntimeError('Scheme not valid')
        self._store['scheme'] = scheme


store = Store()
http_store = HttpStore()


__all__ = ['store', 'http_store']
