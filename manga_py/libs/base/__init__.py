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
from typing import overload
from pathlib import Path


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
            ua = self.arg('user-agent')
            if ua:
                self._http.ua = ua
        return self._http

    def archive_ext(self, name) -> str:
        ext = '.zip'
        if self.arg('cbz'):
            ext = '.cbz'
        return str(Path(name).with_suffix(ext))


    @overload
    def download(self, file: Chapter):
        self.before_download(file)
        self.http.download(file.url, self.archive_ext(file.name))
        self.after_download(file)

    def download(self, file: File):
        self.before_download(file)
        self.http.download(file.url, file.path_location_with_name)
        if not self.arg('not-change-files-xtension'):
            ext = Image.real_extension(file.path_location_with_name)
            _name = file.name
            file.name = '{}.{}'.format(_name[:_name.rfind('.')], ext)
        self.after_download(file)  # split-image
        # args.get('split_image') and img.auto_split()
        Image.process(file, self._args)
