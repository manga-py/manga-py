from .html import Html


class Simplify:
    _content = None
    _manga_name = None
    """
    :property http: Http
    """

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

