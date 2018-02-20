from src.provider import Provider
from .helpers.std import Std


class ManhwaCo(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        return self.re.search(r'\.co/[^/]+/([^/]+)', chapter).group(1)

    def get_main_content(self):
        return self.http_get('{}/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.co/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self._elements('.list-group .list-group-item')

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        items = self._elements('img.img-fluid', content)
        n = self.http().normalize_uri
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.row > div > img.img-responsive')


main = ManhwaCo
