from abc import ABCMeta

from manga_py.libs.http import Http
from .abstract import Abstract
from .callbacks import Callbacks
from .html import Html
from .simplify import Simplify


class Base(Abstract, Callbacks, Simplify, metaclass=ABCMeta):
    _chapters = None
    _files = None
    _http = None
    _html = None

    def __init__(self):
        super().__init__()

    @property
    def html(self) -> Html:
        return Html(self._http)

    @property
    def http(self) -> Http:
        if self._http is None:
            self._http = Http()
        return self._http
