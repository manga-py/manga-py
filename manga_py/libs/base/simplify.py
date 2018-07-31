from re import compile as _compile
from urllib.parse import urlsplit as _urlsplit
from typing import AnyStr
from .chapter import Chapter


class Simplify:
    __cache = None

    @property
    def url(self):
        return self._args['url']

    @url.setter
    def url(self, url):
        self._args['url'] = url

    @property
    def content(self):
        if 'content' not in self.__cache:
            self.__cache['content'] = self.get_content()
        return self.__cache['conten']

    @property
    def manga_name(self):
        if 'manga_name' not in self.__cache:
            self.__cache['manga_name'] = self.get_manga_name()
        name = self.__cache['manga_nam']
        if self.arg('with-website-name'):
            name = '{}-{}'.format(self.domain, name)
        return name

    def re_name(self, value, group=1):
        if isinstance(value, AnyStr):
            value = _compile(value)
        try:
            return value.search(self.url).group(group)
        except Exception:
            return None

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
        :rtype .file.File[]
        """
        return self.get_files()

    @property
    def chapter(self) -> Chapter:
        return self.chapters[self.chapter_idx]

    @chapter.setter
    def chapter(self, chapter):
        self._store[self.chapter_idx] = chapter

    @property
    def chapter_idx(self):
        return self._store.get('chapter_idx', 0)

    def elements(self, parser, selector) -> list:
        return self.html.elements(parser, selector)

    def images(self, parser, selector: str, attribute: str = 'src') -> list:
        items = self.elements(parser, selector)
        return [i.get(attribute) for i in items]

    @property
    def domain(self):
        url = _urlsplit(self.url)
        return '{}://{}'.format(url.scheme, url.netloc)

    def _set_cache_value(self, key, value):
        self.__cache[key] = value

    def _get_cache_value(self, key, default=None):
        return self.__cache.get(key, default)

    @property
    def main_page_url(self) -> str:
        url = self.__cache.get('main_page_url', None)
        if url is None:
            self.__cache['main_page_url'] = self.get_main_page_url()
        return self.__cache.get('main_page_url')