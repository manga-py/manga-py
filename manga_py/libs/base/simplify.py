from .html import Html
from typing import overload
from re import compile as re_compile


class Simplify:
    _content = None
    _manga_name = None

    @property
    def url(self):
        return self.arg('url', None)

    @property
    def content(self):
        if self._content is None:
            self._content = self.get_content()
        return self._content

    @property
    def manga_name(self):
        if self._manga_name is None:
            self._manga_name = self.get_manga_name()
        return self._manga_name

    def images(self, parser, selector: str, attribute: str = 'src'):
        items = Html(self.http).elements(selector, parser)
        return [i.get(attribute) for i in items]

    @overload
    def re_name(self, value: str, group=1):
        _re = re_compile(value)
        return self.re_name(value, group)

    def re_name(self, value, group=1):
        try:
            return value.search(self.url).group(group)
        except Exception:
            return None

    @property
    def chapters(self):
        if self._chapters is None:
            self._chapters = self.get_chapters()
        return self._chapters

    @property
    def files(self):
        return self.get_files()
