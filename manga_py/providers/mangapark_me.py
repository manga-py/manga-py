from manga_py.provider import Provider
from .helpers.std import Std


class MangaParkMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/s.+?(?:/v(\d+))?/c(\d+[^/]*)'
        idx = self.re.search(selector, self.chapter)
        return '{}-{}'.format(
            1 if idx[0] is None else idx[0],
            idx[1]
        )

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('div.stream:last-child em a:last-child')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#viewer img.img')

    def get_cover(self):
        return self._cover_from_content('.cover img')


main = MangaParkMe
