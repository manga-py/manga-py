from urllib.parse import urlsplit
from requests import Response
from typing import List

from manga_py.libs import fs


class Simplify:  # Few hacks to simplify life.
    """
    :type _args dict
    :type __cache dict
    :type get_content callable
    :type get_manga_name callable
    :type get_chapters callable
    :type get_files callable
    :type get_main_page_url callable
    :type get_cover callable
    :type arg callable
    :type _store dict
    :type html manga_py.libs.base.html.Html
    """
    _args = None
    get_content = None
    get_manga_name = None
    arg = None
    _store = None
    html = None
    get_chapters = None
    get_main_page_url = None
    get_cover = None
    get_files = None

    __cache = None

    def __init__(self):
        super().__init__()
        self.__cache = {}

    @property
    def url(self) -> str:
        return self._args['url']

    @url.setter
    def url(self, url):
        """
        Allows you to fix url manga inside the provider.
        It is desirable to make corrections in the before_provider method
        """
        self._args['url'] = url

    @property
    def content(self) -> Response:
        if 'content' not in self.__cache:
            self.__cache['content'] = self.get_content()
        return self.__cache['content']

    @property
    def manga_name(self) -> str:
        if 'manga_name' not in self.__cache:
            self.__cache['manga_name'] = self.get_manga_name()
        if self.arg('with-website-name'):
            return '{}-{}'.format(self.domain, self.__cache['manga_nam'])
        return self.__cache['manga_name']

    @property
    def chapters(self) -> list:
        """
        see manga_py/libs/base/abstract:get_chapters
        :rtype Chapter[]
        """
        if 'chapters' not in self.__cache:
            self.__cache['chapters'] = self.get_chapters()
        return self.__cache['chapters']

    @property
    def files(self) -> list:
        """
        see manga_py/libs/base/abstract:get_chapters
        """
        if 'files' not in self.__cache or self.chapter_idx != self.__cache.get('files', (-1, ''))[0]:
            self.__cache = self.chapter_idx, self.get_files()
        return self.__cache['files'][1]

    @property
    def chapter(self) -> dict:
        """
        TODO
        """
        return self.chapters[self.chapter_idx]

    @chapter.setter
    def chapter(self, chapter):
        self._store[self.chapter_idx] = chapter

    @property
    def chapter_idx(self) -> int:
        return self._store.get('chapter_idx', 0)

    def elements(self, parser, selector) -> list:
        return self.html.elements(parser, selector)

    def images(self, parser, selector: str, attribute: str = 'src') -> List[str]:
        items = self.elements(parser, selector)
        return [i.get(attribute) for i in items]

    @property
    def domain(self) -> str:
        url = urlsplit(self.url)
        return '{}://{}'.format(url.scheme, url.netloc)

    def _set_cache_value(self, key, value):
        self.__cache[key] = value

    def _get_cache_value(self, key, default=None):
        return self.__cache.get(key, default)

    @property
    def main_page_url(self) -> str:
        url = self.__cache.get('main_page_url', None)
        if url is None:
            url = self.__cache['main_page_url'] = self.get_main_page_url()
        return url

    @property
    def cover(self) -> str:
        url = self.__cache.get('cover', None)
        if url is None:
            self.__cache['cover'] = self.get_cover()
        return self.__cache['cover']

    @property
    def meta(self) -> str:
        url = self.__cache.get('meta', None)
        if url is None:
            self.__cache['meta'] = self.get_cover()
        return self.__cache['meta']

    # DEFAULT
    def get_chapter_name(self, chapter) -> str:
        name = fs.basename(chapter.get('url'))
        return fs.remove_query(name)
