from re import compile
from manga_py.provider import Provider
from .helpers.std import Std
from lxml.html import HtmlElement


_RE_IMAGES = compile(r'html_data\s?\+=\s?[\'"](.+)[\'"]')
_RE_DISPLAY_NONE_CLASS = compile(r'.(\w+) { display: none; }')


def html_encoder(data: list):
    out = ''
    for i in ''.join(data).split('.'):
        if i == '':
            continue
        out += chr(int(i, 16))
    return out


class ManaTokiNet(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def get_content(self):
        content = self.http_get(self.get_url())
        parser = self.document_fromstring(content)
        manga_root_url = parser.cssselect('#goNextBtn ~ a[href*="/comic/"]')
        if manga_root_url is None or len(manga_root_url) == 0:
            return content
        return self.http_get(parser[0].get('href'))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.view-title .view-content > span[style] > b')

    def get_chapters(self):
        items = self._elements('.list-body .list-item')
        return [self.__chapter(i) for i in items]

    def __chapter(self, i):
        return (
            self.http().normalize_uri(i.cssselect('a.item-subject')[0].get('href')),
            self.element_text_content(i.cssselect('.wr-num')[0])
        )

    def get_files(self):
        content = self.http_get(self.chapter[0])
        data = _RE_IMAGES.findall(content)
        images = html_encoder(data)
        parser = self.document_fromstring(images)
        hidden_class = _RE_DISPLAY_NONE_CLASS.search(content)
        return self._manatoki_images(parser, hidden_class)

    def _manatoki_images(self, parser: HtmlElement, hidden_class):
        if hidden_class is not None:
            hidden_class = hidden_class.group(1)
        images = []
        for i in parser.cssselect('img'):  # type: HtmlElement
            for k in i.keys():
                if k.startswith('data-'):
                    # filter hidden elements
                    elem_class = i.getparent().get('class')
                    if hidden_class is not None and elem_class is not None and hidden_class == elem_class:
                        break
                    images.append(i.get(k))
                    break
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.view-content1 img')

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = ManaTokiNet
