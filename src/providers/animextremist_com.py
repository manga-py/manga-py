from src.provider import Provider
from .helpers import animextremist_com
from .helpers.std import Std


class AnimeXtremistCom(Provider, Std):
    helper = None
    prefix = '/mangas-online/'

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search(r'(.+?-\d+)', chapter[0])
        return idx.group(1) if idx else '0'

    def get_manga_url(self):
        return '{}{}{}/'.format(self.get_domain(), self.prefix, self.get_manga_name())

    def get_main_content(self):
        return self.http_get(self.get_manga_url())

    def get_manga_name(self) -> str:
        return self.re.search(r'{}([^/]+)'.format(self.prefix), self.get_url()).group(1)

    def get_chapters(self):
        ch = self.helper.get_chapters()
        return ch[::-1]

    def get_files(self):
        chapter = self.get_current_chapter()
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


main = AnimeXtremistCom
