from lxml.html import document_fromstring, HtmlElement, HTMLParser
from manga_py.libs.http import Http


class Html:
    def __init__(self, http: Http):
        self.http = http

    def content(self, content, selector: str = None, idx: int = None):
        html = document_fromstring(content)
        if selector is not None:
            html = html.cssselect(selector)
            if idx is not None and len(html) > idx:
                return html[idx]
        return html

    def url(self, url, selector: str = None, idx: int = None):
        content = self.http.get(url).text
        return self.content(content, selector, idx)

    def elements(self, selector, parser=None):
        if isinstance(parser, str):
            parser = document_fromstring(parser)
        elif not isinstance(parser, (HtmlElement, HTMLParser)):
            raise AttributeError('Undefined type "parser"')
        return parser.cssselect(selector)

    def cover(self, element):
        pass

