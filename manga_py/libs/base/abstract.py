from abc import abstractmethod
from typing import List, Union
from requests import Response

from .manga import Manga
from manga_py.libs.http import Http


class Abstract:

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_main_page_url(self) -> str:
        """
        Returns manga main page url.

        For example:

        http://example.org/manga/manga-name/chapter1.html
        ->
        http://example.org/manga/manga-name.html

        :return:
        """
        pass

    @abstractmethod
    def get_content(self) -> Response:  # mixed
        """
        Returns mixed data on the main page.
        Used in methods get_manga_name, get_chapters, get_cover, get_meta
        Ideally, the main page is requested only once.
        (Use self.content to get data from the provider)

        Must correct the address of the main page if the user did not pass it correctly.
        (For example, instead of the address of the main page of the manga,
         the address of one of the chapters was given.
         Call self.url = 'http://example.org/manga/here' for this)
        :return:
        """
        pass

    @abstractmethod
    def get_manga_name(self) -> str:
        """
        Returns the 'user-friendly' name of the manga.
        Ideally, it is called only once. (Use self.manga_name to get data from the provider)
        :return:
        """
        pass

    @abstractmethod
    def get_chapters(self) -> list:
        """
        Returns the list of chapters.
        Ideally, it is called only once. (Use self.chapters to get data from the provider)

        The method is required to return a list of the form:
        [etree.Element, ...]
        or
        [('absolute_url', 'archive_name/forlder_name'), ...]
        or
        [('absolute_url', ('0', '1', 2, 3), ...]  # chapter idx
        or
        [('absolute_url', 'archive_name/forlder_name'), etree.Element, ...]

        or (for download archive, without images) NOT MIXED WITH PREV!
        [{'url': 'absolute_url', 'name': 'archive_name'}, {'url': 'absolute_url', 'name': 'archive_name'}]

        The latter is not recommended, but can be used.
        :return:
        """
        pass

    @abstractmethod
    def get_files(self) -> list:
        """
        The method is required to return a list of the form:
        [etree.Element, ...]
        or
        [('absolute_url', 'relative_file_name'), ...]
        or
        [('absolute_url', 'relative_file_name'), etree.Element, ...]

        The latter is not recommended, but can be used.
        :return:
        """
        pass

    @abstractmethod
    def get_chapter_name(self, chapter) -> str:
        """
        Returns the current name of the chapter.
        It is called at each iteration of the chapter list. (Use self.chapter to get RAW data from the provider)
        :return:
        :rtype str
        """
        pass

    def get_chapter_url(self) -> str:
        """
        Used to overload the standard behavior.
        Returns the current url of the chapter.
        It is called at each iteration of the chapter list. (Use self.chapter to get RAW data from the provider)
        :return:
        """
        pass

    def before_provider(self, args: dict) -> None:
        """
        The method will be called once, <b>before</b> any other methods in the provider.\
        Will not be automatically called for API! The developer must do it himself.
        :return:
        """
        pass

    def after_provider(self) -> None:
        """
        The method will be called once, <b>after</b> any other methods in the provider.
        Will not be automatically called for API! The developer must do it himself.
        :return:
        """
        pass

    def get_cover(self) -> Union[str, list]:
        """
        Returns the cover of the manga, if possible.
        :return:
        :rtype str or str[] or None
        """
        raise NotImplementedError

    def get_meta(self) -> Manga:  # Todo
        """
        :return:
        :rtype Manga or None
        """
        raise NotImplementedError

    @staticmethod
    def search(title: str, http: Http) -> List[str]:
        """
        Returns the list of manga if search is possible on the site.
        :param title: str
        :return:
        """
        raise NotImplementedError
