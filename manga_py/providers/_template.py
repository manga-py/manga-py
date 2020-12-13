from manga_py.provider import Provider
from .helpers.std import Std


class _Template(Provider, Std):
    def get_archive_name(self) -> str:
        """
        Allows you to overload name generation. Method may be missing
        """

    def get_chapter_index(self) -> str:
        """
        Any string separated by "-"
        Example: "1-3"
        """

    def get_content(self):
        """
        Called second. Returns the initial content to parse (just a cache)
        Can be obtained using self.content
        """

    def get_manga_name(self) -> str:
        """
        String for the name of the manga directory
        """

    def get_chapters(self):
        """
        Should return an array of data (you can return the result of the self._elements ('css selector') method)
        """
        # return self._elements('a.chapter')
        return []

    def get_files(self):
        """
        Should return an array of strings (url of images)
        """
        return []

    def get_cover(self) -> str:
        """Not used now"""
        # return self._cover_from_content('.cover img')

    def book_meta(self) -> dict:
        """
        Not used now
        :see http://acbf.wikia.com/wiki/Meta-data_Section_Definition
        return {
            'author': str,
            'title': str,
            'annotation': str,
            'keywords': str,
            'cover': str,
            'rating': str,
          }
        """

    def chapter_for_json(self) -> str:
        """
        overload std param, if need
        If present, overloads getting chapter name for json dump
        Should return a string
        """
        # return self.chapter
        pass


main = _Template
