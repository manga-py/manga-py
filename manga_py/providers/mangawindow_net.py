from manga_py.provider import Provider
from .helpers.std import Std


class MangaWindowNet(Provider, Std):
    __url = None

    def get_chapter_index(self) -> str:
        return self.chapter[0].replace('.', '-')

    def get_main_content(self):
        return self.http_get(self.__url)

    def get_manga_name(self) -> str:
        title = self.html_fromstring(self.get_url(), '.item-title > a, .nav-title > a', 0)
        self.__url = self.http().normalize_uri(title.get('href'))
        return title.text_content().strip()

    def get_chapters(self):
        items = self._elements('.chapter-list a.chapt')
        result = []
        re = self.re.compile(r'[Cc]h\.(\d+(?:\.\d+)?)')
        n = self.http().normalize_uri
        for i in items:
            text = i.cssselect('b')[0].text_content()
            if 'deleted' not in text.casefold():
                result.append((
                    re.search(text).group(1),
                    n(i.get('href')),
                ))
        return result

    def get_files(self):
        re = self.re.compile(r'images\s*=\s*({.+});')
        content = self.http_get(self.chapter[1])
        items = self.json.loads(re.search(content).group(1))
        return [items[i] for i in sorted(items, key=lambda i: int(i))]

    def get_cover(self) -> str:
        return self._cover_from_content('.attr-cover > img')

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self) -> str:
        return self.chapter[1]


main = MangaWindowNet
