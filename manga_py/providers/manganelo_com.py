from manga_py.provider import Provider
from .helpers.std import Std
from .helpers.manganelo_com_helper import check_alternative_server


class MangaNeloCom(Provider, Std):
    chapter_re = r'[/-]chap(?:ter)?[_-](\d+(?:\.\d+)?)'
    _prefix = '/manga/'
    __alternative_cdn = 'https://bu2.mkklcdnbuv1.com'

    def get_chapter_index(self) -> str:
        return self.re.search(self.chapter_re, self.get_chapter())\
            .group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}%s{}' % self._prefix)

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.panel-story-chapter-list a')

    def get_files(self):
        chapter = self.get_chapter()

        parser = self.html_fromstring(chapter)
        images = self._images_helper(parser, '.container-chapter-reader img')
        return check_alternative_server(images, self.__alternative_cdn, headers={
            'Referer': chapter,
            'Accept': 'image/webp,*/*',
        })

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-info-pic img')

    def get_chapter(self):
        return self.chapter


main = MangaNeloCom
