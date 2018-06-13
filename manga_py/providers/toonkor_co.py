from manga_py.crypt.base_lib import BaseLib
from manga_py.provider import Provider
from .helpers.std import Std


class ToonKorCo(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'\.co/[^_]+_(.+)\.html?')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.co/([^_]+)')

    def get_chapters(self):
        items = self._elements('#fboardlist td.episode__index')
        n = self.http().normalize_uri
        return [n(i.get('data-role')) for i in items]

    def get_files(self):
        content = self.http_get(self.chapter)
        imgs = self.re.search(r'toon_img\s=\s["\'](.+?)["\']', content)
        if not imgs:
            return []
        content = BaseLib.base64decode(imgs.group(1)).decode()
        n = self.http().normalize_uri
        return [n(i.get('src')) for i in self._elements('img', content)]

    def get_cover(self) -> str:
        return self._cover_from_content('.bt_thumb a img')

    def book_meta(self) -> dict:
        pass


main = ToonKorCo
