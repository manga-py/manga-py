from manga_py.provider import Provider
from .helpers.std import Std


class ComicPunchNetManga(Provider, Std):
    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chapter_(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.page-title')

    def get_chapters(self):
        return self._elements('.manga_chapter a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.picture')

    def get_cover(self) -> str:
        return self._cover_from_content('.field-name-field-pic img')


main = ComicPunchNetManga
