from abc import ABCMeta
from pathlib import Path
from urllib.parse import urlparse

from manga_py.libs.crypt.base_lib import BaseLib
from manga_py.libs.http import Http
from manga_py.libs.modules.image import Image
from .abstract import Abstract
from .callbacks import Callbacks
from manga_py.libs.html import Html
from .methods import Methods
from .simplify import Simplify


class Base(Abstract, Methods, Callbacks, Simplify, metaclass=ABCMeta):
    files = None
    chapter = None

    _chapters = None
    _http = None
    _html = None

    _image_process_callbacks = None
    """
    Contains a list of callback functions with priority in the work.
    Each function should return the path to the processed image.
    Those. eg:
    The function (1) receives the path /path/to/file.enc, but returns /path/to/image.png
    The following function (2) will receive /path/to/image.png if the previous one has completed successfully.
    In case of an error, the function (1) call stack will be written to the log.
    Also in this case, the following function (2) will get the path /path/to/file.enc
    This will allow you to have multiple handlers for the same file.
    
    ---
    
    Содержит список callback функций с приоритетом в работе.
    Каждая функция должна вернуть путь к обработанному изображению.
    Т.е. например:
    Функия (1) получает путь /path/to/file.enc, но возвращает /path/to/image.png
    Следующая функция (2) получит /path/to/image.png, если предыдущая завершилась успешно.
    В случае ошибки (1), в лог будет записан стек вызовов функции.
    Также в этом случае следующая функция (2) получит путь /path/to/file.enc
    Это позволит иметь несколько обработчиков одного файла.
    """

    def __init__(self):
        super().__init__()
        _image_process_callbacks = []

    @property
    def html(self) -> Html:
        return Html(self.http)

    @property
    def http(self) -> Http:
        if self._http is None:
            self._http = Http(self.url)
            self._http.set_headers({})
            ua = self.arg('user-agent')
            if ua:
                self._http.ua = ua
        return self._http

    def archive_ext(self, name) -> str:
        ext = '.zip'
        if self.arg('cbz'):
            ext = '.cbz'
        return str(Path(name).with_suffix(ext))

    def download(self, file):
        self.before_download(file)
        self.http.download(file.url, file.path_location)
        self.after_download(file)

        success = True
        path = file.path_location
        for callback in self._image_process_callbacks:
            try:
                path, success = callback(path, success)
            except Exception as e:
                self.logger.error(e.__traceback__)
                success = False

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
        return self.__class__.__name__ + BaseLib.md5('{}{}{}'.format(
            url.netloc,
            url.path.strip('/'),
            url.query,
        )).hexdigest()
