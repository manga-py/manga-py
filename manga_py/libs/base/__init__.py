from abc import ABCMeta

from manga_py.libs.http import Http
from .abstract import Abstract
from .callbacks import Callbacks
from .html import Html
from .simplify import Simplify
from .methods import Methods
from manga_py.libs import fs
from .chapter import Chapter
from .file import File


class Base(Abstract, Methods, Callbacks, Simplify, metaclass=ABCMeta):
    files = None
    chapter = None

    _chapters = None
    _http = None
    _html = None

    def __init__(self):
        super().__init__()

    @property
    def html(self) -> Html:
        return Html(self.http)

    @property
    def http(self) -> Http:
        if self._http is None:
            self._http = Http(self.url)
        return self._http

    def download(self, file):
        self.before_file_save(url, idx)
        self.http.download(url, path_location)
        self.after_file_save(path_location, idx)
