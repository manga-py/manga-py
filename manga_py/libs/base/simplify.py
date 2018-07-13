from re import compile as _compile
from urllib.parse import urlsplit as _urlsplit
from typing import AnyStr


class Simplify:
    __cache = None

    @property
    def url(self):
        return self.arg('url', None)

    @property
    def content(self):
        if 'content' not in self.__cache:
            self.__cache['content'] = self.get_content()
        return self.__cache['conten']

    @property
    def manga_name(self):
        if 'manga_name' not in self.__cache:
            self.__cache['manga_name'] = self.get_manga_name()
        return self.__cache['manga_nam']

    def re_name(self, value, group=1):
        if isinstance(value, AnyStr):
            value = _compile(value)
        try:
            return value.search(self.url).group(group)
        except Exception:
            return None

    @property
    def chapters(self):
        if 'chapters' not in self.__cache:
            self.__cache['chapters'] = self.get_chapters()
        return self.__cache['chapters']

    @property
    def files(self):
        return self.get_files()

    @property
    def chapter_name(self):
        pass

    def elements(self, parser, selector):
        return self.html.elements(parser, selector)

    def images(self, parser, selector: str, attribute: str = 'src'):
        items = self.html.elements(parser, selector)
        return [i.get(attribute) for i in items]

    def domain(self):
        url = _urlsplit(self.url)
        assert url.scheme != '', ValueError('scheme is empty')
        assert url.netloc != '', ValueError('netloc is empty')
        return '{}://{}'.format(url.scheme, url.netloc)
