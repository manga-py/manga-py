from abc import ABCMeta

from manga_py.libs.http import Http
from .abstract import Abstract
from .callbacks import Callbacks
from .html import Html
from .simplify import Simplify
from .methods import Methods
from .chapter import Chapter
from .file import File
from manga_py.libs.modules.image import Image


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

    def download(self, file: File):
        self.before_download(file)
        self.http.download(file.url, file.path_location)
        if not self.arg('not_change_files_extension'):
            ext = Image.real_extension(file.path_location)
            _name = file.path_location
            file.name = '{}.{}'.format(_name[:_name.rfind('.')], ext)
        self.after_download(file)
