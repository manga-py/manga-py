from manga_py.provider import Provider
from .helpers.std import Std


class _Template(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.re.search(r'-chapter-(\d+(?:\.\d+)?)', self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([\w-]+)')

    def get_chapters(self):
        return self._elements('ul a[href*="/chapter/"]')

    def get_files(self):
        parser = self.html_fromstring(self.chapter, '#arraydata', 0)
        content = self.element_text_content(parser)

        if content is None:
            return []

        return content.split(',')

    def get_cover(self) -> str:
        return self._cover_from_content('.imgdesc > img')


main = _Template
