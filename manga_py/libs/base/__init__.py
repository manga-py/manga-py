from abc import ABCMeta
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from manga_py.libs.crypt.base_lib import BaseLib
from manga_py.libs.http import Http
from manga_py.libs.modules.image import Image
from .abstract import Abstract
from .callbacks import Callbacks
from .chapter import Chapter
from .file import File
from .html import Html
from .methods import Methods
from .simplify import Simplify


class Base(Abstract, Methods, Callbacks, Simplify, metaclass=ABCMeta):
    files = None
    chapter = None

    _chapters = None
    _http = None
    _html = None

    # def __init__(self):
    #     super().__init__()

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

    def download(self, item: Union[File, Chapter]):
        if isinstance(item, File):
            self._download_file(item)
        elif isinstance(item, Chapter):
            self._download_chapter(item)
        else:
            raise ValueError(type(item))

    def _download_file(self, file: File):
        self.before_download(file)
        self.http.download(file.url, file.path_location)
        if not self.arg('not-change-files-xtension'):
            ext = Image.real_extension(file.path_location)
            _name = file.name
            file.name = '{}.{}'.format(_name[:_name.rfind('.')], ext)
        self.after_download(file)  # split-image
        # args.get('split_image') and img.auto_split()
        Image.process(file, self._args)

    def _download_chapter(self, chapter: Chapter):
        self.before_download(chapter)
        self.http.download(chapter.url, self.archive_ext(chapter.path_location))
        self.after_download(chapter)

    def _db_key(self) -> str:  # max ~150 characters
        """
        Returns the unique key of the manga.
        Do not repeat with different manga!
        Used to identify the manga in the database

        Overload this if need different key

        :return:
        :rtype: str
        """
        url = urlparse(self.main_page_url)
        return self.__class__.__name__ + BaseLib.md5('{}{}{}{}'.format(
            url.netloc,
            url.path.strip('/'),
            url.query,
            url.fragment,
        ))
