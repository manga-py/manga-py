from manga_py.provider import Provider
from .helpers.std import Std


class ComicOrg(Provider, Std):
    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return 'Album_18comic {}'.format(self._get_name(r'/album/(\d+)'))

    def get_chapters(self):
        elements = self._elements('.episode > ul a[href^="/photo/"]')
        n = self.http().normalize_uri
        return list(set(map(lambda x: n(x.get('href')), elements)))[::-1]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.panel-body img[id]', 'data-original', 'src')

    def get_cover(self) -> str:
        return self._cover_from_content('.thumb-overlay img')


main = ComicOrg
