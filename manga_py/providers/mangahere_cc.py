from manga_py.provider import Provider
from .helpers.std import Std


class MangaHereCc(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

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
        return parser.cssselect('img#image')[0].get('src')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = parser.cssselect('.go_page select.wid60 option + option')
        pages_list = [value.get('value') for value in pages]
        first_image = self.__get_img(parser)
        images = [first_image]
        for i in pages_list:
            parser = self.html_fromstring(i)
            images.append(self.__get_img(parser))
        return images

    def get_cover(self):
        return self._cover_from_content('.manga_detail_top > img')

    def prepare_cookies(self):
        self._base_cookies()


main = MangaHereCc
