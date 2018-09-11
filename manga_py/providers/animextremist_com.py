from manga_py.provider import Provider
from .helpers import animextremist_com
from .helpers.std import Std


class AnimeXtremistCom(Provider, Std):
    helper = None
    prefix = '/mangas-online/'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search(r'(.+?-\d+)', chapter[0])
        return idx.group(1) if idx else '0'

    def get_main_content(self):
        return self._get_content('{}%s{}/' % self.prefix)

    def get_manga_name(self) -> str:
        return self._get_name(r'{}([^/]+)'.format(self.prefix))

    def get_chapters(self):
        ch = self.helper.get_chapters()
        return ch[::-1]

    def get_files(self):
        chapter = self.chapter
        items = self.helper.sort_images(chapter[1])
        images = []
        for i in items:
            img = self.helper.get_page_image(i, 'img#photo')
            img and images.append(img)
        return images

    def prepare_cookies(self):
        self.helper = animextremist_com.AnimeXtremistCom(self)

    def get_cover(self) -> str:
        pass
        # return self._cover_from_content('.cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = AnimeXtremistCom
