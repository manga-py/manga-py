from requests import Response
from abc import abstractmethod
from pathlib import Path
import re
from typing import Optional, List, Callable
from typing import Tuple
from manga_py.libs.img import Img

from manga_py.cli.args.args_helper import ArgsListHelper
from manga_py.exceptions import JsonException
from manga_py.libs.http import Http
from manga_py.libs.log import logger
from manga_py.libs.provider.file_tuple import *
from manga_py.libs.fs import temp_path
from manga_py.libs.store import store


class Provider:
    __slots__ = ('arguments', 'http', '_url', 'logger', 'print', 'store')

    def __init__(self, arguments: ArgsListHelper, url: str):
        self.arguments = arguments
        self.http = Http(self, url)
        self._url = url
        self.logger = logger()
        self.store = store
        self.print = print
        """
        SUPPORTED_URLS: contains a list of possible urls with which the provider works
        Must be set in child classes
        
        Example:
        [
            r'manga-site.example/manga/.',
            r'manga2.example/(?:manga|comics)/',
        ]
        """

    def set_print(self, _print: Callable[..., None] = print):
        self.print = _print

    @classmethod
    def new(cls, store: ArgsListHelper, url: str):
        return cls(store, url)

    def match(self) -> bool:
        for i in self.supported_urls():
            if re.match(r'(?:https?://)?' + i, self._url):
                return True
        return False

    def prepare(self):
        """
        Will be called at the very beginning
        Can change some parameters of the provider
        """
        pass

    def get_main_content(self):
        """
        mixed content
        if site have api, use it
        """
        content = self.http.get(self.main_url()).content  # type: Response
        if self.is_api_site():
            try:
                return content.json()
            except Exception:
                self.logger.warning('JSON content broken %s ' % content)
                raise JsonException(content)
        return content

    def main_url(self) -> str:
        return self._url

    def files_referer(self) -> Optional[str]:
        """
        can turn off the referer for files (require some sites)
        """
        return self._url

    def content_referer(self) -> Optional[str]:
        """
        can turn off the referer for pages (require some sites)
        """
        return self._url

    def is_api_site(self) -> bool:
        return False

    def pages(self) -> List[str]:
        return [self.main_url()]

    # region: Abstract methods

    @staticmethod
    @abstractmethod
    def supported_urls() -> List[str]:
        raise AttributeError('SUPPORTED_URLS is None')

    @abstractmethod
    def manga_name(self) -> str:
        pass

    @abstractmethod
    def chapters(self) -> List[ChapterTuple]:
        pass

    @abstractmethod
    def chapter_files(self, chapter: ChapterTuple) -> ChapterFilesTuple:
        """
        :param chapter: ChapterTuple

        Example:

        [
         ChapterFilesTuple(images=['https://site.example/image.png', ...], archive='https://site.example/archive.zip'),
        ]

        """
        pass

    # endregion

    def download(self, idx: str, url: str, destination: Path, file_type: int) -> FileTuple:
        """ The download is very stupid and just does what it does =) """
        idx, url, destination = self.before_download(idx, url, destination, file_type)
        if self.arguments.simulate:
            return self.after_download(idx, destination, file_type)
        self.http.download(self.http.get(url), destination)
        return self.after_download(idx, destination, file_type)

    def before_download(self, idx: str, url: str, path: Path, file_type: int) -> Tuple[str, str, Path]:
        """
        Must return arguments
        May change file location or url
        :param str idx: file index
        :param str url:
        :param Path path:
        :param int file_type:
        """
        return idx, url, path

    def after_download(self, idx: str, path: Path, file_type: int) -> FileTuple:
        """
        Can check file for correctness (for example, its size)
        Should also be used to decrypt files

        may return multiple images
        (for example, an image can be split into two or the archive can be unpacked)

        :param str idx: file index
        :param str path:
        :param int file_type:
        """
        if TYPE_IMAGE:
            _path = Img(path).path_with_real_format()
            if _path is not path:
                path.rename(_path)
                path = _path

        return FileTuple(idx, [path], file_type)

    @staticmethod
    def temp_path(url: str = None) -> Path:
        if url is not None:
            return temp_path().joinpath('{}-%s' % Path(url).name)
        return temp_path()


__all__ = ['Provider']
