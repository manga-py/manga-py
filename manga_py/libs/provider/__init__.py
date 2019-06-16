import json
from abc import abstractmethod
from pathlib import Path
from re import match
from typing import Optional, List, Tuple

from manga_py import exceptions
from manga_py.cli.args import ArgsListHelper
from manga_py.libs.http import Http
from manga_py.libs.log import logger


class Provider:
    __slots__ = ('arguments', 'http', '_url', 'SUPPORTED_URLS')
    TYPE_IMAGE = 'image'
    TYPE_ARCHIVE = 'archive'

    def __init__(self, store: ArgsListHelper, url: str):
        self.arguments = store
        self.http = Http(url)
        self._url = url
        self.SUPPORTED_URLS = None  # type: List[str]
        self.SUPPORTED_URLS.__doc__ = """
        SUPPORTED_URLS: contains a list of possible urls with which the provider works
        Must be set in child classes
        
        Example:
        [
            r'manga-site.example/manga/.',
            r'manga2.example/(?:manga|comics)/',
        ]
        """

    @classmethod
    def new(cls, store: ArgsListHelper, url: str):
        return cls(store, url)

    @classmethod
    def match(cls, url) -> bool:
        if cls.SUPPORTED_URLS is None:
            logger().warning('SUPPORTED_URLS is None for provider %s', cls.__class__.__name__)
        for i in cls.SUPPORTED_URLS:
            if match(i, url):
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
        content = self.http.get(self.main_url()).content
        if self.is_api_site():
            try:
                return json.loads(content)
            finally:
                exceptions.JsonException(content)
        return content

    def main_url(self) -> str:
        return self.main_url()

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

    @abstractmethod
    def manga_name(self) -> str:
        pass

    @abstractmethod
    def chapters(self) -> List[str]:
        pass

    @abstractmethod
    def chapter_files(self, idx, url) -> List[dict]:
        """
        :param int idx: Chapter index
        :param str url: Chapter url

        Example:

        [
         {self.TYPE_IMAGE: 'https://site.example/image.png'},
         {self.TYPE_ARCHIVE: 'https://site.example/archive.zip'},
        ]

        """
        pass

    # endregion

    def download(self, idx: int, url: str, destination: Path):
        """ The download is very stupid and just does what it does =) """
        idx, url, destination = self.before_download(idx, url, destination)
        if self.arguments.simulate:
            return self.after_download(idx, destination)
        self.http.download(self.http.get(url), destination)
        return self.after_download(idx, destination)

    def before_download(self, idx: int, url: str, destination: Path) -> Tuple[int, str, Path]:
        """
        Must return arguments
        May change file location or url
        :param idx:
        :param url:
        :param destination:
        """
        return idx, url, destination

    def after_download(self, idx: int, destination: Path) -> Tuple[int, Path]:
        """
        Can check file for correctness (for example, its size)
        Should also be used to decrypt files
        :param idx:
        :param destination:
        """
        return idx, destination
