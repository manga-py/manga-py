from manga_py.provider import Provider
from .helpers.std import Std


class MangaHereCc(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/[^\d]+(\d+)'
        chapter = self.chapter
        return self.re.search(selector, chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail_list .left a')

    @staticmethod
    def __get_img(parser):
        return [i.get('src') for i in parser.cssselect('img#image')]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, '.go_page select.wid60', True)
        first_image = self.__get_img(parser)
        images = first_image
        n = self.http().normalize_uri
        for page in pages:
            parser = self.html_fromstring(n(page.get('value')))
            images += self.__get_img(parser)
        return images

    def get_cover(self):
        return self._cover_from_content('.manga_detail_top > img')

    def prepare_cookies(self):
        self._base_cookies()

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHereCc
