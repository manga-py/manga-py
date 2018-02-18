from src.provider import Provider
from .helpers import animextremist_com
from .helpers.std import Std


class AnimeXtremistCom(Provider, Std):
    helper = None
    prefix = '/mangas-online/'

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        print(chapter)
        exit()
        return r'(.+?-\d+)'

    def get_manga_url(self):
        return '{}{}{}/'.format(self.get_domain(), self.prefix, self.get_manga_name())

    def get_main_content(self):
        return self.http_get(self.get_manga_url())

    def get_manga_name(self) -> str:
        return self.re.search(r'{}([^/]+)'.format(self.prefix), self.get_url()).group(1)

    def std_get_chapters(self):
        return self._chapters('li > a + a')[::-1]

    def get_chapters(self):
        return self.helper.get_chapters()

    def get_files(self):
        chapter = self.get_current_chapter()
        return []

    def prepare_cookies(self):
        self.helper = animextremist_com.AnimeXtremistCom(self)

    def get_cover(self) -> str:
        pass
        # return self._cover_from_content('.cover img')


main = AnimeXtremistCom
