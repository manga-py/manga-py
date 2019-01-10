from manga_py.provider import Provider
from .helpers.std import Std


class ManhwaHentaiCom(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(r'/chapter-(\d+(?:-\d+)?)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manhwa/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'./manhwa/([^/]+)')

    def get_chapters(self):
        return self._elements('.version-chap > li > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.reading-content .wp-manga-chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image img.img-responsive')

    def book_meta(self) -> dict:
        pass


main = ManhwaHentaiCom
