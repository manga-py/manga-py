from manga_py.provider import Provider
from .helpers.std import Std


class MangaNeloCom(Provider, Std):
    chapter_re = r'[/-]chap(?:ter)?[_-](\d+(?:\.\d+)?)'
    _prefix = '/manga/'

    def get_chapter_index(self) -> str:
        return self.re.search(self.chapter_re, self.get_chapter())\
            .group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}%s{}' % self._prefix)

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.panel-story-chapter-list a')

    def get_files(self):
        parser = self.html_fromstring(self.get_chapter())
        images = self._images_helper(parser, '.container-chapter-reader img')
        if not len(images):
            raise NotImplementedError  # TODO: Just don't know what to do here
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-info-pic img')

    def get_chapter(self):
        return self.chapter


main = MangaNeloCom
