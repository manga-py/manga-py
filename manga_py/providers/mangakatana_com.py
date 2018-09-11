from manga_py.provider import Provider
from .helpers.std import Std


class MangaKatanaCom(Provider, Std):
    name_re = r'/manga/([^/]+)'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/.+?\d/c(\d+(?:\.\d)?(?:-v\d)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        return self.http_get('{}/manga/{}'.format(
            self.domain, self._name()
        ))

    def get_manga_name(self) -> str:
        name = self._name()
        return name[:name.rindex('.')]

    def get_chapters(self):
        return self._elements('.chapters .chapter a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.wrap_img > img', 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img')

    def book_meta(self) -> dict:
        pass

    def _name(self):
        return self.re.search(self.name_re, self.get_url()).group(1)


main = MangaKatanaCom
